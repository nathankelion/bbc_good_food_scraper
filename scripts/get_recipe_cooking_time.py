import re
from lxml import html

# Get cooking time
def get_recipe_cooking_time(response):
    # Convert the soup to an lxml element tree
    tree = html.fromstring(response.content)
    
    # Locate the cook and prep times
    prep_times = tree.xpath('/html/body/div/div[4]/main/div[2]/section/div/div[4]/ul[1]/li[1]/div/div[2]/ul/li[1]/span[2]/time')
    cook_times = tree.xpath('/html/body/div/div[4]/main/div[2]/section/div/div[4]/ul[1]/li[1]/div/div[2]/ul/li[2]/span[2]/time')

    cook = []
    prep = []
    cook_HH_mm = []
    prep_HH_mm = []
    
    # Extract and print the text content of cook element(s)
    for time_element in cook_times:
        cook.append(time_element.text)

    # Extract and print the text content of prep element(s)
    for time_element in prep_times:
        prep.append(time_element.text)

    # Function to convert a time string to hours and minutes
    def get_hours_and_minutes(time_str):
        hours, minutes = 0, 0
        match_hr = re.search(r'(\d+) hr', time_str)
        if match_hr:
            hours = int(match_hr.group(1))
        match_min = re.search(r'(\d+) mins', time_str)
        if match_min:
            minutes = int(match_min.group(1))
        return hours, minutes

    # Process cooking times
    for time_str in cook:
        hours, minutes = get_hours_and_minutes(time_str)
        cook_HH_mm.append((hours, minutes))

    # Process prep times
    for time_str in prep:
        hours, minutes = get_hours_and_minutes(time_str)
        prep_HH_mm.append((hours, minutes))

    # Calculate the average cooking time
    avg_cook_hours = sum(hours for hours, _ in cook_HH_mm) / max(len(cook_HH_mm), 1)
    avg_cook_minutes = sum(minutes for _, minutes in cook_HH_mm) / max(len(cook_HH_mm), 1)

    # Calculate the average prep time
    avg_prep_hours = sum(hours for hours, _ in prep_HH_mm) / max(len(prep_HH_mm), 1)
    avg_prep_minutes = sum(minutes for _, minutes in prep_HH_mm) / max(len(prep_HH_mm), 1)

    # Calculate total hours and minutes
    total_hours = int(avg_cook_hours + avg_prep_hours)
    total_minutes = int(avg_cook_minutes + avg_prep_minutes)

    # Calculate carryover from minutes to hours
    total_hours += total_minutes // 60
    total_minutes %= 60

    # Convert the total hours and minutes back to HH:mm format
    total_hh_mm_format = f'{total_hours:02d}:{total_minutes:02d}'

    return total_hh_mm_format