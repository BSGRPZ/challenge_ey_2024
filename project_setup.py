#!/usr/bin/env python3

import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

import requests
import yaml
from tqdm import tqdm

data_dir = Path("data")
archive_dir = Path.joinpath(data_dir, "archive")


def download_file(url, output_dir, filename):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(
        total=total_size_in_bytes, unit="iB", unit_scale=True, desc=filename
    )
    with open(os.path.join(output_dir, filename), "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()


def process_file(file_path, output_dir):
    if zipfile.is_zipfile(file_path):
        extract_file(file_path, output_dir)
        shutil.move(file_path, archive_dir)


def extract_file(file_path, extract_dir):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        total_size = sum(file.file_size for file in zip_ref.infolist())
        progress_bar = tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Extracting", leave=False
        )
        for file in zip_ref.infolist():
            zip_ref.extract(file, extract_dir)
            progress_bar.update(file.file_size)
        progress_bar.close()


def download_data(yaml_file):
    os.makedirs(archive_dir, exist_ok=True)

    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)
        with ThreadPoolExecutor() as executor:
            futures = []
            for key in data:
                output_dir = Path.joinpath(data_dir, key)
                os.makedirs(output_dir, exist_ok=True)
                for url in data[key]:
                    filename = url.split("/")[-1]
                    futures.append(
                        executor.submit(download_file, url, output_dir, filename)
                    )
            wait(futures)
            for key in data:
                for url in data[key]:
                    filename = url.split("/")[-1]
                    file_path = Path.joinpath(data_dir, key, filename)
                    process_file(file_path, file_path.parent)


if __name__ == "__main__":
    download_data(Path.joinpath(data_dir, "links.yaml"))
