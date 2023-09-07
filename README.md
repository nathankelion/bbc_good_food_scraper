# BBC Good Food Recipe Scraper

This Python package scrapes the BBC Good Food website to extract information about recipes that match specific filters. It collects data such as recipe names, cooking times, dietary categories, difficulty levels, nutritional information, and more. The scraped data is then cleaned and stored in various CSV files within the `output` folder.

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

## Installation

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
    python -m venv bbc_good_food_venv
    bbc_good_food_venv\Scripts\activate  # On Windows
    source bbc_good_food_venv/bin/activate  # On macOS and Linux
    ```

4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

To run the scraper, use the following command:
```
python recipe_scraping_script.py
```

The script will scrape data from the BBC Good Food website based on the specified filters, clean the data, and store it in the output folder as CSV files.

When you're finished with the package, you can deactivate the virtual environment by running:
```
deactivate
```
This will return you to the system-wide Python environment.

## Project Structure

The project structure is as follows:
- output/: This folder contains the CSV files where the scraped data is stored.
- scripts/: This folder contains the Python functions used for scraping and data processing.
- recipe_scraping_script.py: The main script for scraping BBC Good Food recipes.
- requirements.txt: A list of required Python packages and their versions.
- README.md: This file, providing information on the project and how to use it.

## Motivation
This project was born out of my passion for health and fitness, and my desire to delve into the data to gain insights into what constitutes "healthy" eating from a nutritional perspective (at least according to the BBC). I wanted to answer questions like: Does preparing "healthy" food require more time in the kitchen? Are there significant variations in protein content among different dietary choices, and if so, do lower-protein diets still meet daily protein requirements?

Through this project, I aim to shed light on these questions by collecting and analysing data from the BBC Good Food website. Ultimately, I plan to visualise this data with a user-friendly dashboard, making it accessible to anyone interested in understanding the nutritional landscape of recipes.

If you share a curiosity about health, nutrition, and cooking, I encourage you to download and use this package to access and explore the data.


## Contact

If you have any questions, suggestions, or feedback related to this project, please feel free to get in touch:

- Nathan Kelion
- nathankelion26@gmail.com
- Project Repository: [GitHub Repository](https://github.com/nathankelion/bbc_good_food)