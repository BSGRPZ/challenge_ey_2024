# EY Challenge 2024 by BSGRPZ

## Description

**TBD**

## Prerequisites

- Poetry, refer to their [installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer)
- Python 3.10

## Installation
It is assumed you are running a Debian based OS

### Virtual environment
The virtual environment and the dependencies are handled by Poetry

```bash
poetry install
```

### Specific installation

#### GDAL

You will need the Python development libraries

```bash
sudo apt-get install python3-dev
```

Install the GDAL native library and development headers

```bash
sudo apt install libgdal-dev
```

Install the GDAL Python package while matching the version number of the GDAL library

```bash
poetry run pip install gdal==$(gdal-config --version)
```

### Dataset setup

To download the necessary files for the dataset into the data directory

```bash
poetry run python3 project_setup.py
```
