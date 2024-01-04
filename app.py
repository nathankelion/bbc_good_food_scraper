import streamlit as st
from sqlalchemy import text
import pandas as pd
from rapidfuzz import process, fuzz, utils

from scripts.sql_query_functions import SQL_query, count_recipes

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Display title
st.title('BBC Good Food Recipe Finder')

# Define the query and call the SQL_query function to get the DataFrame with recipe information
main_query = text('''
        SELECT ri.recipe_id, ri.RecipeName, ri.CookingTime, ri.HealthStatus, ri.Diet, ri.Difficulty, n.kcal, n.[Fat(g)], n.[Saturates(g)], n.[Carbs(g)], n.[Sugars(g)], n.[Fibre(g)], n.[Protein(g)], n.[Salt(g)], ri.RecipeLink
        FROM recipe_info    AS ri
        JOIN nutrition      AS n ON ri.recipe_id = n.recipe_id
    ''')
result_df = SQL_query(main_query)

# Define the query and call the SQL_query function to get the DataFrame with ingredient information
ingredient_query = text('''
        SELECT *
        FROM ingredients
    ''')
ingredients_df = SQL_query(ingredient_query)

# Radio button to choose between searching for a recipe or an ingredient
search_type = st.radio("Select Search Type", ["Search Recipe", "Search Ingredient"])

if search_type == "Search Recipe":
    # Add a recipe search bar
    search_query = st.text_input("Search Recipe Name", "")
elif search_type == "Search Ingredient":
    # Add an ingredient search bar with a multiselect box
    new_ingredient = st.text_input("Enter an ingredient", "")

# Add a title to the sidebar
st.sidebar.title('Filter Options')

# Add filters
# Cooking time tickbox
selected_cooking_times = st.sidebar.multiselect('Select Cooking Time(s)', ['<= 30 minutes' ,'30 minutes - 1 hour', '1-2 hours', '2-3 hours', '3-4 hours', '> 4 hours'])

# Health Status drop-down
health_status = st.sidebar.selectbox('Health Status', ["I don't mind",'Healthy'])

# Diet drop-down
selected_diet = st.sidebar.selectbox('Select Diet', ["I don't mind", 'Regular', 'Vegetarian (inc. Vegan)', 'Vegan'])

# Difficulty boxes
selected_difficulties = st.sidebar.multiselect('Select Difficult(y/ies)', ['Not given', 'Easy', 'More effort', 'A challenge'])

# Would you like nutritional sliders to show?
nutrition_filters = st.sidebar.checkbox('Show/Hide Nutrition Filters')

# Create boxes for filtering by nutrition values
if nutrition_filters:
    kcals = st.sidebar.multiselect('How many Calories?', ['<= 250 kcal', '250-500 kcal', '500-750 kcal', '750-1000 kcal', '> 1000 kcal'])
    fat_content = st.sidebar.multiselect('How much Fat?', ['<= 10 g', '10-20 g', '20-30 g', '30-40 g', '> 40 g'])
    saturates_content = st.sidebar.multiselect('How much Saturated Fat?', ['<= 2 g', '2-4 g', '4-6 g', '6-8 g', '8-10 g', '> 10 g'])
    carbs_content = st.sidebar.multiselect('How many Carbs?', ['<= 15 g', '15-30 g', '30-45 g', '45-60 g', '60-75 g', '> 75 g'])
    sugars_content = st.sidebar.multiselect('How much Sugars?', ['<= 5 g', '5-10 g', '10-15 g', '15-20 g', '> 20 g'])
    fibre_content = st.sidebar.multiselect('How much Dietary Fiber?', ['<= 2 g', '2-4 g', '4-6 g', '6-8 g', '8-10 g', '> 10 g'])
    protein_content = st.sidebar.multiselect('How much Protein?', ['<= 10 g', '10-20 g', '20-30 g','30-40 g', '40-50 g', '> 50 g'])
    salt_content = st.sidebar.multiselect('How much Salt?', ['<= 1 g', '1-2 g', '2-3 g', '3-4 g', '> 4 g'])

# Add a "Remove All Filters" button
if st.sidebar.button('Remove All Filters'):
    cooking_time = []
    health_status = "I don't mind"
    selected_diet = "I don't mind"
    selected_difficulties = []
    nutrition_filters = []

# Add a button to clear the search box
if st.button("Clear Search"):
    search_query = ""
    new_ingredient = ""

# Apply Filters
# Apply Search Query using rapidfuzz
if search_type == "Search Recipe" and search_query:
    # Get a list of recipe names from the DataFrame
    recipe_names = result_df['RecipeName'].tolist()

    # Use rapidfuzz to get the best matches with scores
    results = process.extract(search_query, recipe_names, scorer=fuzz.token_set_ratio, processor=utils.default_process, limit=None)

    if results:
        # Filter matches with scores higher than 50
        threshold = 60
        filtered_results = [(name, score) for name, score, _ in results if score >= threshold]

        if filtered_results:
            # Sort filtered results by score in descending order
            filtered_results.sort(key=lambda x: x[1], reverse=True)
            st.success("Best Matches:")

            # Create a list of matching recipe names
            matching_names = [name for name, _ in filtered_results]

            # Create a custom ordering column based on the order of matching_names
            result_df['CustomOrder'] = pd.Categorical(result_df['RecipeName'], categories=matching_names, ordered=True).codes

            # Filter the DataFrame to include only matching recipes
            result_df = result_df[result_df['RecipeName'].isin(matching_names)].sort_values(by='CustomOrder').drop(columns='CustomOrder')

        else:
            st.warning("No results found.")
            result_df = pd.DataFrame()  # Empty DataFrame to display

# Apply ingredients filter
if search_type == "Search Ingredient" and new_ingredient:

    # List of ingredients to search for
    ingredients_to_search = [new_ingredient]

    # Create a boolean mask for each ingredient
    ingredient_masks = [ingredients_df['Ingredient'].str.contains(ingredient, case=False) for ingredient in ingredients_to_search]

    # Combine masks using the any condition
    combined_mask = pd.concat(ingredient_masks, axis=1).all(axis=1)
    
    # Apply the mask to filter recipe_info
    result_df = result_df[result_df['recipe_id'].isin(ingredients_df.loc[combined_mask, 'recipe_id'])]

# Apply Cooking Time filter
if selected_cooking_times:
    # Define your cooking time filters
    cooking_time_filters = {
        '<= 30 minutes': result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) <= 30,
        '30 minutes - 1 hour': (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) > 30) & (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) <= 60),
        '1-2 hours': (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) > 60) & (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) <= 120),
        '2-3 hours': (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) > 120) & (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) <= 180),
        '3-4 hours': (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) > 180) & (result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) <= 240),
        '> 4 hours': result_df['CookingTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])) > 240
    }

    cooking_time_filter = pd.Series(data=False, index=result_df.index)
    for selected_time in selected_cooking_times:
        cooking_time_filter |= cooking_time_filters[selected_time]

    # Apply the combined filter to the DataFrame
    result_df = result_df[cooking_time_filter]

# Apply Health filter
if health_status != "I don't mind":
    result_df = result_df[result_df['HealthStatus'] == health_status]

# Apply Diet filter
if selected_diet == 'Vegetarian (inc. Vegan)':
    result_df = result_df[result_df['Diet'].isin(['Vegetarian', 'Vegan'])]
elif selected_diet != "I don't mind":
    result_df = result_df[result_df['Diet'] == selected_diet]

# Apply Difficulty Filter
if selected_difficulties:
    result_df = result_df[result_df['Difficulty'].isin(selected_difficulties)]

# Apply Nutrition filters
if nutrition_filters:
    # Filter based on Calories
    kcal_filters = {
    '<= 250 kcal': result_df['kcal'] <= 250,
    '250-500 kcal': (result_df['kcal'] > 250) & (result_df['kcal'] <= 500),
    '500-750 kcal': (result_df['kcal'] > 500) & (result_df['kcal'] <= 750),
    '750-1000 kcal': (result_df['kcal'] > 750) & (result_df['kcal'] <= 1000),
    '> 1000 kcal': result_df['kcal'] > 1000
    }

    if kcals:
        kcal_filter = pd.Series(data=False, index=result_df.index)
        for selected_kcal in kcals:
            kcal_filter |= kcal_filters[selected_kcal]

        # Apply the combined filter to the DataFrame
        result_df = result_df[kcal_filter]

    # Filter based on Fat content
    fat_filters = {
        '<= 10 g': result_df['Fat(g)'] <= 10,
        '10-20 g': (result_df['Fat(g)'] > 10) & (result_df['Fat(g)'] <= 20),
        '20-30 g': (result_df['Fat(g)'] > 20) & (result_df['Fat(g)'] <= 30),
        '30-40 g': (result_df['Fat(g)'] > 30) & (result_df['Fat(g)'] <= 40),
        '> 40 g': result_df['Fat(g)'] > 40
    }

    if fat_content:
        fat_filter = pd.Series(data=False, index=result_df.index)
        for selected_fat in fat_content:
            fat_filter |= fat_filters[selected_fat]

        # Apply the combined filter to the DataFrame
        result_df = result_df[fat_filter]

    # Filter based on Saturated Fat content
    saturates_filters = {
        '<= 2 g': result_df['Saturates(g)'] <= 2,
        '2-4 g': (result_df['Saturates(g)'] > 2) & (result_df['Saturates(g)'] <= 4),
        '4-6 g': (result_df['Saturates(g)'] > 4) & (result_df['Saturates(g)'] <= 6),
        '6-8 g': (result_df['Saturates(g)'] > 6) & (result_df['Saturates(g)'] <= 8),
        '8-10 g': (result_df['Saturates(g)'] > 8) & (result_df['Saturates(g)'] <= 10),
        '> 10 g': result_df['Saturates(g)'] > 10
    }

    if saturates_content:
        saturates_filter = pd.Series(data=False, index=result_df.index)
        for selected_saturates in saturates_content:
            saturates_filter |= saturates_filters[selected_saturates]

        # Apply the combined filter to the DataFrame
        result_df = result_df[saturates_filter]

    # Filter based on Carbs content
    carbs_filters = {
        '<= 15 g': result_df['Carbs(g)'] <= 15,
        '15-30 g': (result_df['Carbs(g)'] > 15) & (result_df['Carbs(g)'] <= 30),
        '30-45 g': (result_df['Carbs(g)'] > 30) & (result_df['Carbs(g)'] <= 45),
        '45-60 g': (result_df['Carbs(g)'] > 45) & (result_df['Carbs(g)'] <= 60),
        '60-75 g': (result_df['Carbs(g)'] > 60) & (result_df['Carbs(g)'] <= 75),
        '> 75 g': result_df['Carbs(g)'] > 75
    }

    if carbs_content:
        carbs_filter = pd.Series(data=False, index=result_df.index)
        for selected_carbs in carbs_content:
            carbs_filter |= carbs_filters[selected_carbs]

        # Apply the combined filter to the DataFrame
        result_df = result_df[carbs_filter]

    # Filter based on Sugars content
    sugars_filters = {
        '<= 5 g': result_df['Sugars(g)'] <= 5,
        '5-10 g': (result_df['Sugars(g)'] > 5) & (result_df['Sugars(g)'] <= 10),
        '10-15 g': (result_df['Sugars(g)'] > 10) & (result_df['Sugars(g)'] <= 15),
        '15-20 g': (result_df['Sugars(g)'] > 15) & (result_df['Sugars(g)'] <= 20),
        '> 20 g': result_df['Sugars(g)'] > 20
    }

    if sugars_content:
        sugars_filter = pd.Series(data=False, index=result_df.index)
        for selected_sugars in sugars_content:
            sugars_filter |= sugars_filters[selected_sugars]

        # Apply the combined filter to the DataFrame
        result_df = result_df[sugars_filter]

    # Filter based on Dietary Fiber content
    fibre_filters = {
        '<= 2 g': result_df['Fibre(g)'] <= 2,
        '2-4 g': (result_df['Fibre(g)'] > 2) & (result_df['Fibre(g)'] <= 4),
        '4-6 g': (result_df['Fibre(g)'] > 4) & (result_df['Fibre(g)'] <= 6),
        '6-8 g': (result_df['Fibre(g)'] > 6) & (result_df['Fibre(g)'] <= 8),
        '8-10 g': (result_df['Fibre(g)'] > 8) & (result_df['Fibre(g)'] <= 10),
        '> 10 g': result_df['Fibre(g)'] > 10
    }

    if fibre_content:
        fibre_filter = pd.Series(data=False, index=result_df.index)
        for selected_fibre in fibre_content:
            fibre_filter |= fibre_filters[selected_fibre]

        # Apply the combined filter to the DataFrame
        result_df = result_df[fibre_filter]

    # Filter based on Protein content
    protein_filters = {
        '<= 10 g': result_df['Protein(g)'] <= 10,
        '10-20 g': (result_df['Protein(g)'] > 10) & (result_df['Protein(g)'] <= 20),
        '20-30 g': (result_df['Protein(g)'] > 20) & (result_df['Protein(g)'] <= 30),
        '30-40 g': (result_df['Protein(g)'] > 30) & (result_df['Protein(g)'] <= 40),
        '40-50 g': (result_df['Protein(g)'] > 40) & (result_df['Protein(g)'] <= 50),
        '> 50 g': result_df['Protein(g)'] > 50
    }

    if protein_content:
        protein_filter = pd.Series(data=False, index=result_df.index)
        for selected_protein in protein_content:
            protein_filter |= protein_filters[selected_protein]

        # Apply the combined filter to the DataFrame
        result_df = result_df[protein_filter]

    # Filter based on Salt content
    salt_filters = {
        '<= 1 g': result_df['Salt(g)'] <= 1,
        '1-2 g': (result_df['Salt(g)'] > 1) & (result_df['Salt(g)'] <= 2),
        '2-3 g': (result_df['Salt(g)'] > 2) & (result_df['Salt(g)'] <= 3),
        '3-4 g': (result_df['Salt(g)'] > 3) & (result_df['Salt(g)'] <= 4),
        '> 4 g': result_df['Salt(g)'] > 4
    }

    if salt_content:
        salt_filter = pd.Series(data=False, index=result_df.index)
        for selected_salt in salt_content:
            salt_filter |= salt_filters[selected_salt]

        # Apply the combined filter to the DataFrame
        result_df = result_df[salt_filter]


# Display subtitle
st.subheader(f'{count_recipes(result_df)} recipes:')

# Display the result as a table
st.write(result_df)

# Add a line with your information, using CSS to position it at the bottom
st.markdown(
    """<div style='position: fixed; bottom: 10px; width: 100%; text-align: center;'><i>This app was created by Nathan Kelion in 2023.<i></div>""",
    unsafe_allow_html=True
)