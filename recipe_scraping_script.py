import requests
import time
import math
import pandas as pd
from bs4 import BeautifulSoup

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
page_list = [3]

# List and Dict for storage
used_recipe_links = []
recipe_names = []
successful_links = []
recipe_cooking_times = []
recipe_nutritional_values = {}
recipe_category_information = {}


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

                # Fill in the dictionary of recipe nutritional values
                for name, value in zip(nutrition_name, nutrition_values):
                    if name.text in recipe_nutritional_values:
                        recipe_nutritional_values[name.text].append(value.text)
                    else:
                        recipe_nutritional_values[name.text] = [value.text]

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


print('Transforming data...')

# Transform the recipe_nutritional_values dict
clean_recipe_nutritional_values = {}
for name, values in recipe_nutritional_values.items():
    if name == 'kcal':
        clean_recipe_nutritional_values[name] = values
    else:
        clean_recipe_nutritional_values[name.capitalize() + ' (g)'] = [value[:-1] for value in values]


# Create a DataFrame for recipe names and links
print('Creating CSV files...')

# Test print statements
print(f'''
        names list is {len(recipe_names)}
        links list {len(successful_links)}
        time list {len(recipe_cooking_times)}
        nutritional list {len(clean_recipe_nutritional_values['kcal'])}
        category list {len(recipe_category_information['Diet'])}
      ''')

recipe_names_df = pd.DataFrame({'Recipe Name': recipe_names, 'Recipe Link': successful_links})

# Create a DataFrame for cooking times
cooking_time_df = pd.DataFrame({'Cooking Time (HH:mm)': recipe_cooking_times})

# Create a DataFrame for nutrition
nutrition_df = pd.DataFrame(clean_recipe_nutritional_values)

# Create a DataFrame for categories
categories_df = pd.DataFrame(recipe_category_information)


# Add recipe_id column based on index to each DataFrame starting from 1
recipe_names_df.insert(0, 'recipe_id', recipe_names_df.index + 1)
cooking_time_df.insert(0, 'recipe_id', cooking_time_df.index + 1)
nutrition_df.insert(0, 'recipe_id', nutrition_df.index + 1)
categories_df.insert(0, 'recipe_id', categories_df.index + 1)

# Specify the file paths for the CSV files
recipe_names_csv = "output/recipe_names.csv"
cooking_time_csv = "output/cooking_time.csv"
nutrition_csv = "output/nutrition.csv"
categories_csv = "output/categories.csv"

# Export DataFrames to CSV files
recipe_names_df.to_csv(recipe_names_csv, index=False)
cooking_time_df.to_csv(cooking_time_csv, index=False)
nutrition_df.to_csv(nutrition_csv, index=False)
categories_df.to_csv(categories_csv, index=False)

print('Scraping completed.')