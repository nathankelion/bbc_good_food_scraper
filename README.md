# BBC Good Food Recipe Scraper

This Python package scrapes the BBC Good Food website to extract information about recipes. It collects data such as recipe names, cooking times, dietary categories, difficulty levels, nutritional information, and more. The scraped data is then transformed and uploaded to a database hosted by AWS RDS.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Motivation](#motivation)
- [Contact](#contact)

## Prerequisites

Before you can use this package, make sure you have the following prerequisites installed on your system:

- **Python 3.11**: You can download and install Python 3.11 from the [official Python website](https://www.python.org/downloads/).

- **pip**: `pip` is the Python package manager and is usually included with Python installations. To check if you have `pip` installed, open a terminal or command prompt and run:

  ```
  pip --version
  ```

If pip is not installed, you can follow the [installation instructions](https://pip.pypa.io/en/stable/installation/) to install it.

- **Microsoft SQL Server Management Studio** connected to a [free tier AWS](https://portal.aws.amazon.com/billing/signup#/start/email) RDS database instance: You can download and install SSMS from the [official Microsoft website](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16) and learn how to connect the two [here](https://www.youtube.com/watch?v=vp_uulb5phM). 

## Installation and Setup

To use this package, follow these steps:

1. Open a terminal or command prompt and clone this GitHub repository to your local machine:
    ```
    git clone https://github.com/nathankelion/bbc_good_food.git
    ```

2. Navigate to the project directory:
    ```
    cd /path/to/your/project/bbc_good_food_scraper
    ```

3. Create and activate a virtual environment (optional but recommended):
    
    If you want to keep the project's dependencies isolated from your system-wide Python installation, it's a good idea to use a virtual environment.
    ```
    # Create virtual environment
    python -m venv bbc_good_food_venv

    # Activate virtual environmnet
    bbc_good_food_venv\Scripts\activate  # On Windows
    source bbc_good_food_venv/bin/activate  # On macOS and Linux
    ```

4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

Create a file called `.env` with the following structure:
```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

Navigate to the `/sql_code/create_tables.sql` open in SSMS and run the queries to create the tables required.

To run the scraper, use the following command:
```
python recipe_scraping_script.py
```

The script will scrape data from the BBC Good Food website based on the specified filters, transform the data, and store it in your database hosted by AWS RDS..

When you're finished with the package, you can deactivate the virtual environment by running:
```
deactivate
```
This will return you to the system-wide Python environment.

Using SQL you can search for recipes using more precise/wider range of filters

## Project Structure

The project structure is as follows:
- scripts/: This folder contains the Python functions used for scraping and data processing.
- sql_code/: This folder contains the sql queries required to create the tables to store scraped data.
- recipe_scraping_script.py: The main script for scraping BBC Good Food recipes.
- requirements.txt: A list of required Python packages and their versions.
- .gitignore: 
- README.md: This file, providing information on the project and how to use it.

## Motivation
This project was born out of my passion for health and fitness, and my frustration at not being able to find recpes on the BBC Good Food website that align with specific macronutrient values. I believe that eating well should be both nutritious AND enjoyable (not just chicken and rice...).

If you share a desire to cook and eat well I encourage you to download and use this package to access and explore the recipes.


## Contact

If you have any questions, suggestions, or feedback related to this project, please feel free to get in touch:

- Nathan Kelion
- nathankelion26@gmail.com
- Project Repository: [GitHub Repository](https://github.com/nathankelion/bbc_good_food)