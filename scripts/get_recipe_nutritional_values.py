# Get the nutritional values
def get_recipe_nutritional_values(soup):
    nutrition_name = soup.find_all('td', attrs={'class': 'key-value-blocks__key'})
    nutrition_values = soup.find_all('td', attrs={'class': 'key-value-blocks__value'})
    return nutrition_name, nutrition_values