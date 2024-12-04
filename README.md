# BBC Good Food Recipe Scraper and Web App

This project consists of two main components: a Python package for scraping the BBC Good Food website to extract recipe information and a Streamlit app that provides a user-friendly interface for non-technical users.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Scraper](#scraper)
  - [Streamlit App](#streamlit-app)
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

- **Microsoft SQL Server Management Studio** (SSMS) connected to a [free tier AWS](https://portal.aws.amazon.com/billing/signup#/start/email) RDS database instance: You can download and install SSMS from the [official Microsoft website](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16) and learn how to connect the two [here](https://www.youtube.com/watch?v=vp_uulb5phM). 

## Installation and Setup

To use this package, follow these steps:

1. Open a terminal or command prompt and clone this GitHub repository to your local machine:
    ```
    git clone https://github.com/nathankelion/bbc_good_food_scraper_and_app.git
    ```

2. Navigate to the project directory:
    ```
    cd /path/to/your/project/bbc_good_food_scraper_and_app
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
### Scraper
Create a file called `.env` with the following structure:
```
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Navigate to the `/sql/create_tables.sql` open in SSMS and run the queries to create the tables required.

To run the scraper, use the following command:
```
python recipe_scraping_script.py
```

The script will scrape data from the BBC Good Food website, transform the data, and store it in your database hosted by AWS RDS.

### Streamlit App
Run the Streamlit app using the following command:
```
streamlit run app.py
```

Visit the provided URL in your web browser to access the Streamlit app.

When you're finished with the package, you can deactivate the virtual environment by running:
```
deactivate
```

This will return you to the system-wide Python environment.

## Project Structure

The project structure is as follows:
- .github/workflows/: This folder contains the .yml file used to automate the running of the recipe scraping script.
- scripts/: This folder contains the Python functions used for scraping, data processing, and database connection.
- sql/: This folder contains the sql queries required to create the tables to store scraped data.
- recipe_scraping_script.py: The main script for scraping BBC Good Food recipes.
- app.py: The script for the Streamlit app.
- requirements.txt: A list of required Python packages and their versions.
- .gitignore: 
- README.md: This file, providing information on the project and how to use it.

## Motivation
This project was born out of my passion for health and fitness, and my frustration at not being able to find recpes on the BBC Good Food website that align with specific macronutrient values. I believe that eating well should be both nutritious AND enjoyable (not just chicken and rice...). Additionally, what if you have specific ingredients in the fridge and want to find a recipe that uses all of them? This will allow you to search for recipes that use specific ingredients, reducing wasted food.

If you share a desire to cook, eat well AND reduce food waste I encourage you to download and use this package to access and explore the recipes.


## Contribute

Feel free to fork this project and make contributions. If you encounter any issues or have ideas for improvement, please open an issue or submit a pull request.

Steps to contribute:
Fork the repository
Clone the forked repository
Create a new branch: git checkout -b feature-branch
Make your changes
Commit your changes: git commit -m "Add feature"
Push to your branch: git push origin feature-branch
Create a pull request
