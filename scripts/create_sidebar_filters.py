import streamlit as st

def create_filters():
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