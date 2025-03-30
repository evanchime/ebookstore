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
     - `python3 ebookstore.py [--database-file "/path_to_database_file" | --connection-url "database_connection_string"] [--table-records "predefined_table_records_file"] [--table-name "table_name"]`
   * Database Options:
     - The path_to_database_file is for SQlite
     - The database_connection_string is for MySQL
   * MySQL Connection String Format:
     - `mysql://user:password@host:port/database`
   * Environment Variable:
     - The database connection string can also be provided in a variable in an environment file with the variable named `MYSQL_CONNECTION_URL`
   * Instructions:
     - Follow the on-screen instructions to interact with the inventory system.
2. Running on Docker Container (Ensure you have root/admin privileges)
   * Connect to SQLite database
     - `docker run -i -v path_to_database_file:/data evanchime/ebookstore --database-file "/data/path_to_database_file" [--table-records "/data/path_to_table_records_file"] [--table-name "table_name"]`
   * Connect to MySQL database from command line
     - `docker run -i [-v path_to_table_records_file:/data] evanchime/ebookstore --connection-url "database_connection_string" [--table-records "/data/path_to_table_records_file"] [--table-name "table_name"]`
   * Connect to MySQL database from an environment file
     - `docker run -i [-v path_to_table_records_file:/data] --env-file path_to_environment_file evanchime/ebookstore [--table-records "/data/path_to_table_records_file"] [--table-name "table_name"]`
     - You can also use Docker Compose with an environment file
     - The database connection string in a variable in an environment file should be named `MYSQL_CONNECTION_URL`
   * MySQL Connection String Format:
     - `mysql://user:password@host:port/database`

![First screenshot of ebookstore](ebookstore_screenshot_1.png)
![Second continuation screenshot of ebookstore](ebookstore_screenshot_2.png)

## Contributing
Contributions are welcome! See the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License. For more information, please refer to the [LICENSE](LICENSE.md) file.
