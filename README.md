# eBookstore

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

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/your-username/ebookstore.git
    ```

2. Navigate to the project directory:
    ```
    cd ebookstore
    ```

3. Install a python virtual enviroment. Optional (recommended). Instruction is for Ubuntu. Proceed according to your enviroment
    ```
    cd your_dev_folder
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
    python3 -m pip freeze -l > requirements.txt
    ```
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Run the main script: `python ebookstore.py database_file [predefined_table_records_file]`
2. Follow the on-screen instructions to interact with the inventory system.

![First screenshot of ebookstore](ebookstore_screenshot_1.png)
![Second continuation screenshot of ebookstore](ebookstore_screenshot_2.png)

## Contributing
Contributions are welcome! See the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License. For more information, please refer to the [LICENSE](LICENSE.md) file.
