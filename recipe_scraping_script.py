import requests
import time
import math
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from scripts.get_recipe_links import get_recipe_links
from scripts.get_recipe_name import get_recipe_name
from scripts.get_recipe_cooking_time import get_recipe_cooking_time
from scripts.get_recipe_nutritional_values import get_recipe_nutritional_values
from scripts.get_recipe_categories import get_recipe_categories


# url of the BBC Good Food recipes page with relevent filters applied (I'm only after main dishes)
filtered_page_url = 'https://www.bbcgoodfood.com/search?tab=recipe&mealType=lunch%2Cvegetable%2Csupper%2Cpasta%2Cmain-course%2Cfish-course%2Cdinner&q=recipes%3Ddinner'
base_url = 'https://www.bbcgoodfood.com'

# Define the maximum number of retry attempts and delay between retries
max_retries = 3
retry_delay = 5  # in seconds

for attempt in range(max_retries):
    try:
        # Get and Parse the HTML using Beautiful Soup
        base_page_response = requests.get(filtered_page_url)
        base_page_response.raise_for_status()
        base_soup = BeautifulSoup(base_page_response.content, 'html.parser')
        
        # Break the retry loop if the request is successful
        break
    except requests.exceptions.RequestException as e:
        print(f"An error occurred for this website: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Max retry attempts reached for {filtered_page_url}. Exiting. Please try again later.")
            exit(1)  # You can choose to exit the script if retries are exhausted

# Add a delay of 1 second after successful request and parsing
time.sleep(1)

# How many pages are there?
results = base_soup.find('p', attrs={'class':'search-results__results-text body-copy-bold mb-md mt-reset d-inline-block'}).text
results_list = results.split()
number_of_recipes = int(results_list[5])
number_of_pages = math.ceil(number_of_recipes / 30)

# list of page numbers
# page_list = list(range(1, number_of_pages + 1))
page_list = [1]


# List and Dict for storage
used_recipe_links = []
recipe_names = []
successful_links = []
recipe_cooking_times = []
recipe_nutritional_data = []
recipe_category_information = {}
nutritional_desired_keys = ["kcal", "fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt"]


# Loop through the base pages
for page_number in page_list:
    print(f'Scraping page {page_number} of {len(page_list)}...')
    page_url = filtered_page_url + '&page=' + str(page_number)

    for attempt in range(max_retries):
        try:
            # Get and Parse the HTML for each page
            page_response = requests.get(page_url)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.content, 'html.parser')
            
            # Break the retry loop if the request is successful
            break
        except requests.exceptions.RequestException as e:
            print(f"An error occurred for this page url: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Max retry attempts reached for {page_url}. Skipping to the next page.")
                break

    # Add a delay of 1 second after successful request and parsing
    time.sleep(1)

    # Create a list of recipe links
    new_recipe_links = []
    links = get_recipe_links(soup, base_url)
    for link in links:
        if link not in used_recipe_links:
            new_recipe_links.append(link)


    # Loop through the recipe link list sending GET requests and parsing the HTML of specific recipes
    for link in new_recipe_links:
        for attempt in range(max_retries):
            try:
                recipe_response = requests.get(link)
                recipe_response.raise_for_status()
                recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')

                recipe_name = get_recipe_name(recipe_soup)
                recipe_names.append(recipe_name)

                recipe_cooking_time = get_recipe_cooking_time(recipe_response)
                recipe_cooking_times.append(recipe_cooking_time)

                nutrition_name, nutrition_values = get_recipe_nutritional_values(recipe_soup)
                categories = get_recipe_categories(recipe_soup)

                # Create an empty dictionary for the current recipe nutrition
                recipe_nutritional_values = {key: None for key in nutritional_desired_keys}

                # Fill in the dictionary of recipe nutritional values
                for name, value in zip(nutrition_name, nutrition_values):
                    if name.text in recipe_nutritional_values:
                        recipe_nutritional_values[name.text] = value.text

                # Add the dictionary for the current recipe to the list
                recipe_nutritional_data.append(recipe_nutritional_values)

                # Fill in the dictionary of recipe category information
                for category, status in categories.items():
                    if category in recipe_category_information:
                        recipe_category_information[category].append(status)
                    else:
                        recipe_category_information[category] = [status]

                # Add link to successful_links list
                successful_links.append(link)

                # Break the retry loop if the request is successful
                break
            except requests.exceptions.RequestException as e:
                print(f"An error occurred for this recipe link: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retry attempts reached for {link}. Moving on to the next link.")
                    break

        # Add the link to the used links list
        used_recipe_links.append(link)

        # Add a delay of 1 second between requests (outside of the retry loop)
        time.sleep(1)


print('Cleaning the data...')

# Initialize the combined dictionary for nutrition with keys
keys = ["kcal", "fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt"]
clean_recipe_nutritional_values = {key: [] for key in keys}

# Iterate through the list of dictionaries
for recipe_data in recipe_nutritional_data:
    for key in keys:
        value = recipe_data.get(key)
        if value is None:
            clean_recipe_nutritional_values[key].append(None)
        else:
            if key != 'kcal':
                value = value[:-1]  # Remove 'g' from values
            clean_recipe_nutritional_values[key].append(value)

# Rename the keys
final_nutrition_dict = {
    "kcal": "kcal",
    "fat": "Fat(g)",
    "saturates": "Saturates(g)",
    "carbs": "Carbs(g)",
    "sugars": "Sugars(g)",
    "fibre": "Fibre(g)",
    "protein": "Protein(g)",
    "salt": "Salt(g)",
}

# Apply the key renaming to the dictionary
final_nutrition_dict = {
    final_nutrition_dict[key]: values
    for key, values in clean_recipe_nutritional_values.items()
}

# Create a DataFrame for recipe information
print('Connecting to Database...')

recipe_info_data = {
    'RecipeName': recipe_names,
    'RecipeLink': successful_links,
    'CookingTime': recipe_cooking_times,
    **recipe_category_information  # Unpack the dictionary
}
recipe_info_df = pd.DataFrame(recipe_info_data)

# Create a DataFrame for nutrition
nutrition_df = pd.DataFrame(final_nutrition_dict)

# Add recipe_id column based on index to each DataFrame starting from 1
recipe_info_df.insert(0, 'recipe_id', recipe_info_df.index + 1)
nutrition_df.insert(0, 'recipe_id', nutrition_df.index + 1)

# Load database variables from .env file
load_dotenv()

# Access database variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Create a SQLAlchemy engine
connection_string = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)
Conn = engine.connect()

# Define table names
recipe_info_table_name = "recipe_info"
nutrition_table_name = "nutrition"


# # Truncate the 'nutrition' table before insertion
# truncate_nutrition_sql = text(f'TRUNCATE TABLE {nutrition_table_name};')
# Conn.execution_options(autocommit=True).execute(truncate_nutrition_sql)

# # Truncate the 'recipe_info' table before insertion
# truncate_recipe_info_sql = text(f'TRUNCATE TABLE {recipe_info_table_name};')
# Conn.execution_options(autocommit=True).execute(truncate_recipe_info_sql)

# Insert new data into the 'recipe_info' table
recipe_info_df.to_sql(recipe_info_table_name, engine, if_exists='append', index=False)
print("Data added to 'recipe_info' table successfully.")

# Insert new data into the 'nutrition' table
nutrition_df.to_sql(nutrition_table_name, engine, if_exists='append', index=False)
print("Data replaced in 'nutrition' table successfully.")


# Dispose of the SQLAlchemy engine to release resources
engine.dispose()