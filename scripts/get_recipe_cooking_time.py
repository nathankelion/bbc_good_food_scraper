import re

# Get cooking time
def get_recipe_cooking_time(soup):
    # Find all <time> elements with a 'datetime' attribute
    cooking_times = soup.find_all('time', attrs={'datetime': lambda value: value is not None})
    raw_list = []
    cooking_times_HH_mm = []
    
    # Extract and print the text content of each element
    for time_element in cooking_times:
        raw_list.append(time_element.text)

    for time_str in raw_list:
        hours, minutes = 0, 0
        
        # Check for hours and extract the numeric value
        match_hr = re.search(r'(\d+) hr', time_str)
        if match_hr:
            hours = int(match_hr.group(1))
        
        # Check for minutes and extract the numeric value
        match_min = re.search(r'(\d+) mins', time_str)
        if match_min:
            minutes = int(match_min.group(1))

        # Convert to HH:mm format
        hh_mm_format = f'{hours:02d}:{minutes:02d}'
        cooking_times_HH_mm.append(hh_mm_format)


    # Initialize variables to store total hours and total minutes
    total_hours = 0
    total_minutes = 0

    # Iterate through the list and add up the hours and minutes
    for hh_mm_format in cooking_times_HH_mm:
        hours, minutes = map(int, hh_mm_format.split(':'))
        total_hours += hours
        total_minutes += minutes

    # Calculate the total hours and minutes
    total_hours += total_minutes // 60
    total_minutes %= 60

    # Convert the total hours and minutes back to HH:mm format
    total_hh_mm_format = f'{total_hours:02d}:{total_minutes:02d}'

    return total_hh_mm_format