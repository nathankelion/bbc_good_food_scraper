# Get a dictionary of recipe categories
def get_recipe_categories(soup):
    categories_dict = {}
    category_text = []
    difficulty_text = []
    categories = soup.find_all('span', attrs={'class': 'terms-icons-list__text d-flex align-items-center'})
    elements = soup.find_all('div', attrs={'class': 'icon-with-text__children'})
    for category in categories:
        category_text.append(category.text)

    if 'Healthy' in category_text:
        categories_dict['Health Status'] = 'Healthy'
    else:
        categories_dict['Health Status'] = None
        
    if 'Vegan' in category_text:
        categories_dict['Diet'] = 'Vegan'
    elif 'Vegetarian' in category_text:
            categories_dict['Diet'] = 'Vegetarian'
    else:
        categories_dict['Diet'] = 'Regular'

    for element in elements:
        difficulty_text.append(element.text)
        
    if 'Easy' in difficulty_text:
        categories_dict['Difficulty'] = 'Easy'
    elif 'More effort' in difficulty_text:
        categories_dict['Difficulty'] = 'More effort'
    elif 'A challenge' in difficulty_text:
        categories_dict['Difficulty'] = 'A challenge'
    else:
        categories_dict['Difficulty'] = 'Not given'
    return categories_dict