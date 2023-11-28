import streamlit as st
from sqlalchemy import text
import pandas as pd
from rapidfuzz import process, fuzz, utils

from scripts.sql_query_functions import SQL_query, count_recipes

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Display title
st.title('BBC Good Food Recipe Finder')

# Define the query and call the SQL_query function to get the DataFrame
# query = text('''
#         SELECT DISTINCT ri.RecipeName, ri.CookingTime, ri.HealthStatus, ri.Diet, ri.Difficulty, n.kcal, n.[Fat(g)], n.[Saturates(g)], n.[Carbs(g)], n.[Sugars(g)], n.[Fibre(g)], n.[Protein(g)], n.[Salt(g)], ri.RecipeLink, Ingredient
#         FROM recipe_info    AS ri
#         JOIN nutrition      AS n ON ri.recipe_id = n.recipe_id
#         JOIN ingredients    AS i ON ri.recipe_id = i.recipe_id
#     ''')

# full_df = SQL_query(query)

# Refine the results 
# result_df = full_df.drop(columns=['Ingredient']).drop_duplicates().reset_index(drop=True)

query = text('''
        SELECT DISTINCT ri.RecipeName, ri.CookingTime, ri.HealthStatus, ri.Diet, ri.Difficulty, n.kcal, n.[Fat(g)], n.[Saturates(g)], n.[Carbs(g)], n.[Sugars(g)], n.[Fibre(g)], n.[Protein(g)], n.[Salt(g)], ri.RecipeLink
        FROM recipe_info    AS ri
        JOIN nutrition      AS n ON ri.recipe_id = n.recipe_id
    ''')
result_df = SQL_query(query)

# Radio button to choose between searching for a recipe or an ingredient
search_type = st.radio("Select Search Type", ["Search Recipe", "Search Ingredient"])

if search_type == "Search Recipe":
    # Add a recipe search bar
    search_query = st.text_input("Search Recipe Name", "")
if search_type == "Search Ingredient":
    # Add an ingredient search bar
    new_ingredient = st.text_input("Enter an ingredient", "")

# Convert 'CookingTime' from str to time




# Add a title to the sidebar
st.sidebar.title('Filter Options')

# Add filters
# Cooking time tickbox
selected_cooking_times = st.sidebar.multiselect('Select Cooking Time(s)', ['< 30 minutes' ,'30 minutes - 1 hour', '1-2 hours', '2-3 hours', '3-4 hours', '> 4 hours'])


# Health Status drop-down
health_status = st.sidebar.selectbox('Health Status', ["I don't mind",'Healthy'])

# Diet drop-down
selected_diet = st.sidebar.selectbox('Select Diet', ["I don't mind", 'Regular', 'Vegetarian (inc. Vegan)', 'Vegan'])

# Difficulty tickboxes
selected_difficulties = st.sidebar.multiselect('Select Difficult(y/ies)', ['Not given', 'Easy', 'More effort', 'A challenge'])

# Would you like nutritional sliders to show?
nutrition_filters = st.sidebar.checkbox('Show/Hide Nutrition Filters')

# Create sliders for filtering by nutrition values
if nutrition_filters:
    kcals = st.sidebar.multiselect('How many Calories?', ['< 250 kcal', '300-500 kcal', '500-750 kcal', '750-1000 kcal', '> 1000 kcal'])
    fat_content = st.sidebar.multiselect('How much Fat?', ['< 10 g', '10-20 g', '20-30 g', '30-40 g', '> 40 g'])
    saturates_content = st.sidebar.multiselect('How much Saturated Fat?', ['< 2 g', '2-4 g', '4-6 g', '6-8 g', '8-10 g', '> 10 g'])
    carbs_content = st.sidebar.multiselect('How many Carbs?', ['< 15 g', '15-30 g', '30-45 g', '45-60 g', '60-75 g', '> 75 g'])
    sugars_content = st.sidebar.multiselect('How much Sugars?', ['< 5 g', '5-10 g', '10-15 g', '15-20 g', '> 20 g'])
    fibre_content = st.sidebar.multiselect('How much Dietary Fiber?', ['< 2 g', '2-4 g', '4-6 g', '6-8 g', '8-10 g', '> 10 g'])
    protein_content = st.sidebar.multiselect('How much Protein?', ['< 10 g', '10-20 g', '20-30 g',' 30-40 g', '40-50 g', '> 50 g'])
    salt_content = st.sidebar.multiselect('How much Salt?', ['< 1 g', '1-2 g', '2-3 g', '3-4 g', '> 4 g'])

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

# Apply Filters
# # Apply Search Query using rapidfuzz
# if search_query:
#     # Get a list of recipe names from the DataFrame
#     recipe_names = result_df['RecipeName'].tolist()

#     # Use rapidfuzz to get the best matches with scores
#     results = process.extract(search_query, recipe_names, scorer=fuzz.partial_ratio, processor=utils.default_process)

#     if results:
#         # Filter matches with scores higher than 50
#         threshold = 10
#         filtered_results = [(name, score) for name, score, _ in results if score >= threshold]

#         if filtered_results:
#             # Sort filtered results by score in descending order
#             filtered_results.sort(key=lambda x: x[1], reverse=True)

#             st.success("Best Matches:")

#             # Create a list of matching recipe names
#             matching_names = [name for name, _ in filtered_results]

#             # Filter the DataFrame to include only matching recipes
#             result_df = result_df[result_df['RecipeName'].isin(matching_names)]
#         else:
#             st.warning("No matches found with a score higher than 50.")
#             result_df = pd.DataFrame()  # Empty DataFrame to display
#     else:
#         st.warning("No matches found.")
#         result_df = pd.DataFrame()  # Empty DataFrame to display


# Apply ingredients filter



# Apply Cooking Time filter



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
# if nutrition_filters:
    


# Display subtitle
st.subheader(f'{count_recipes(result_df)} recipes:')

# Display the result as a table
st.write(result_df)

# Add a line with your information, using CSS to position it at the bottom
st.markdown(
    """<div style='position: fixed; bottom: 10px; width: 100%; text-align: center;'><i>This app was created by Nathan Kelion in 2023.<i></div>""",
    unsafe_allow_html=True
)