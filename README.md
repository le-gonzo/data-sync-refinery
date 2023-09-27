# DataSyncRefinery

`DataSyncRefinery` is a robust ETL framework tailored for modern data workflows. While orchestration tools like Airflow enable execution of ETL processes, DataSyncRefinery empowers developers by providing a standardized, modular, and Pythonic approach to designing the actual ETL scripts.

## Core Principles:
- **Complement, Not Compete**: Designed to work seamlessly alongside orchestration tools without being inherently tied to any specific one.
- **Standardization at Forefront**: Introduces a common methodology to ETL design, ensuring consistency and quality across data operations.
- **Security and Flexibility**: Supports environment-based configurations ensuring credentials are kept safe and can adapt to various security protocols.
- **Extensible Connectivity**: Comes bundled with modules for generic database connections, API interactions, and GUI-based web portal sign-ins
- **End-to-end Modules**: Offers abstracted modules for data extraction, a library of transformation tools, and versatile data loading mechanisms.

## Features

- **Extensible Extractors**: Supports extraction from APIs, flat files (CSV, Excel), and database systems.
- **Powerful Transformers**: Provides functionalities like data cleaning, merging, enrichment, and normalization.
- **Flexible Loaders**: Facilitates data loading into databases, data warehouses, and visualization tools.
- **Robust Connection Management**: Efficiently manages connections to various data sources and destinations.

## Getting Started

### Prerequisites

- List any software, libraries, or tools that need to be installed.
- Mention required versions or compatibility notes.

### Installation

1. **Clone the Repository**:
    ```
    git clone [repository-url]
    ```

2. **Navigate to the Directory**:
    ```
    cd data-sync-refinery
    ```

3. **Setup a Virtual Environment** (optional but recommended):
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

4. **Install Dependencies**:
    ```
    pip install -r requirements.txt  # If you have a requirements file
    ``````

5. **Setup Configuration Settings***
   
   - Copy the `config.ini.template` file and rename the copy to `config.ini`.
   - Edit `config.ini` and replace placeholders with appropriate values. See: `CONFIGURATION.md`.

### Usage

TO-DO: Provide a step-by-step guide on how to use the project. For instance:

1. Configure your data sources in `config.py`.
2. Run the main ETL process:
    ```
    python main.py
    ```

### Configuration

TO-DO: Briefly explain the configuration parameters and how users can modify them to suit their needs.

## Development

### Directory Structure

Here's an overview of the main directories and their purposes:

- `/data-sync-refinery`: The root directory of the project.
    - `/etl`: Contains all the main ETL logic components.
        - `/base`: Holds the base class and foundational utilities for the ETL processes.
            - `etl_base.py`: The abstract base class for ETL operations.
            - `error_logger.py`: Utility for logging and managing errors during ETL processes.
        - `/utilities`: Directory for utility classes and helper functions.
            - `connection_manager.py`: Manages connections to different data sources and destinations.
        - `/extractors`: Contains classes responsible for data extraction from various sources.
            - `api_extractor.py`: Extracts data from APIs.
            - `file_extractor.py`: Reads data from flat files, e.g., CSV, Excel.
            - `database_extractor.py`: Fetches data from database systems.
        - `/transformers`: (Expand with individual files when created) Contains classes to transform and process the extracted data.
        - `/loaders`: (Expand with individual files when created) Includes classes for loading the transformed data into desired destinations.
        - `etl_runner.py`: Orchestrates the end-to-end ETL process, linking extractors, transformers, and loaders.
    - `/config_management`:
        - `abstract_manager.py`: Contains the `AbstractSecretManager` class.
        - `aws_manager.py`: Implementation for AWS Secrets Manager (`AWSSecretManager` class).
        - `azure_manager.py`: Implementation for Azure Key Vault (`AzureKeyVaultManager` class).
        - `gcp_manager.py`: Implementation for Google Cloud Secret Manager.
        - `factory.py`: Contains the `get_secret_manager` factory function.
    - `/tests`: Directory for all unit and integration tests. (Expand on specifics when you have detailed tests)
    - `environment.yml`: Conda environment configuration detailing project dependencies.
    - `config.ini`: Configuration settings for the ETL processes, such as data source details and connection parameters.
    - `main.py`: The main entry point for executing ETL jobs.
    - `README.md`: Provides an overview and instructions for the project.
    - `LICENSE.txt`: GNU GPL v3 license.
    - `.gitignore` 

### Testing

TO-DO: Explain how developers can run tests.

## Contributions

TO-DO: State if you're open to contributions and how others can contribute to the project. Provide guidelines if any.

## License

Copyright (C) 2023 Luis Enrique Gonzalez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

## Acknowledgments

Shout out to any tools, libraries, or individuals that played a significant role in the development of the project.
