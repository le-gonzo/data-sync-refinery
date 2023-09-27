# Configuration Guide - `DataSyncRefinery`

This document outlines the various configuration settings available for the `DataSyncRefinery` project and how to set them up.

## Table of Contents
1. [config.ini](#configini)
    - [Secrets](#secrets)

## config.ini
The main configuration file for the project. Ensure it's located in the root directory of the project.

### Secrets
Section for secret management tool configurations.

**SECRET_MANAGER**: Specifies the secret management tool in use.
- **Type**: String
- **Allowed Values**: 'AWS', 'AZURE'
- **Example**: `SECRET_MANAGER = AWS`
- **Description**: Determines which secret manager implementation to use. It should match one of the secret manager providers available in the project.


---

### How to Set Up:

1. Copy the `config.ini.template` file and rename the copy to `config.ini`
2. Edit `config.ini` and replace placeholders with appropriate values.

**Note**: Always keep your configuration files secure and avoid exposing sensitive information. If using Git, ensure the `config.ini` is listed in the `.gitignore` to prevent unintentional pushes to public repositories.
