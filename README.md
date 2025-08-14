# eBookstore

[![Publish ebookstore Docker image](https://github.com/evanchime/ebookstore/actions/workflows/publish_ebookstore_docker_image.yml/badge.svg)](https://github.com/evanchime/ebookstore/actions/workflows/publish_ebookstore_docker_image.yml)
[![GitHub Release](https://img.shields.io/github/v/release/evanchime/ebookstore)](https://github.com/evanchime/ebookstore/releases/latest)

Welcome to eBookstore, a Python project for managing a bookstore.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
eBookstore is a command-line application with a user-friendly interface that allows a bookstore clerk to manage the stores inventory

## Features
- Add new books to the database
- Update book information
- Delete books from the database
- Search the database to find a specific book
- User has the choice of using either SQLite or MySQL database.

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/evanchime/ebookstore.git
    ```

2. Navigate to the project directory:
    ```
    cd ebookstore
    ```

3. Install a python virtual enviroment. Optional (recommended). Instruction is for Ubuntu. Proceed according to your enviroment
    ```
    sudo apt install python3-venv
    python3 -m venv my_env
    source my_env/bin/activate
    ```

    Remember to deactivate the environment when you're done:
    ```
    deactivate
    ```

4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Running Directly on Your Localhost
   * Run the main script: 
     - `python3 ebookstore.py --database-file "/path_to_database_file"`
   * Instructions:
     - Follow the on-screen instructions to interact with the inventory system.
   * For more advanced usage and available command-line arguments, please run:
     - `python3 ebookstore.py --help`
2. Running on Docker Container (Ensure you have root/admin privileges)
   * Run the container:
     - `docker run -i -v path_to_database_file:/data evanchime/ebookstore:latest --database-file "/data/path_to_database_file"`
   * Instructions:
     - Follow the on-screen instructions to interact with the inventory system.
   * For more advanced usage and available command-line arguments, please run:
     - `docker run evanchime/ebookstore:latest --help`

### Stable & Reproducible Docker Usage (Recommended for Production)

For use in scripts or production, we strongly recommend pinning to a specific version tag. This ensures you are always running a predictable, stable version. **Our latest release is shown in the badge at the top of this page.**

There are two main strategies for pinning your version:

**1. Pinning to a Minor Version (e.g., `:vX.X`)**

This approach gives you a balance of stability and automatic security updates. The `:vX.X` tag will always point to the latest patch release within the `X.X.X` series. 

```sh
# This will pull the latest patch for vX.X (e.g., vX.X.1, then vX.X.2 later)
# Update the version number to match the latest release badge!
docker pull evanchime/ebookstore:vX.X
```

**2. Pinning to a Specific Patch Version (e.g., :vX.X.X)**

This is the most stable and reproducible method. The :vX.X.X tag is an immutable pointer to a single, specific release and will never change. This is the best choice for critical systems where you must guarantee that the running code is exactly the same every time.

```sh
# This will ALWAYS pull the exact vX.X.X release and nothing else
# Update the version number to match the latest release badge!
docker pull evanchime/ebookstore:vX.X.X
```

![First screenshot of ebookstore](ebookstore_screenshot_1.png)
![Second continuation screenshot of ebookstore](ebookstore_screenshot_2.png)

## Contributing
Contributions are welcome! See the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License. For more information, please refer to the [LICENSE](LICENSE.md) file.
