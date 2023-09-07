# Get a list of recipe links
def get_recipe_links(soup, base_url):
    recipe_links_list = []
    recipe_ext = soup.find_all('a', attrs={'class':'link d-block'})
    for ext in recipe_ext:
        recipe_url = base_url + ext['href']
        recipe_links_list.append(recipe_url)
    recipe_links_list = recipe_links_list[:-3]
    return recipe_links_list