import re

# Get a list of cooking times
def get_recipe_cooking_times(soup):
    cooking_times_list = []
    cooking_times = soup.find_all('span', attrs={'class': 'terms-icons-list__text d-flex align-items-center'})
    for time in cooking_times:
        time_text = time.text
        if re.search(r'[1-9]', time_text):
            cooking_times_list.append(time_text)
    return cooking_times_list