from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep 
import pandas as pd
import re
import os 
from math import floor

def check_background_color(cell):
    background_color = cell.value_of_css_property('background-color')
    if background_color == 'rgba(0, 255, 0, 0.3)':
        return 'OK'
    else:
        if cell.text =='':
            return '0'
        return cell.text

def extract_number(string):
    pattern = r'\((\d+)\)'
    match = re.search(pattern, string)
    if match:
        return int(match.group(1))
    else:
        return None
    
def add_percentage(num_solved: str, col: str):
    text = num_solved
    val: int = 0
    den = extract_number(col)
    if text == 'OK':
        val = den
    elif text != '':
        val = int(text)
    if den and den > 0:
        text = f"{val} : {((val/den)*100):.2f} %"
    return text

def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def interpolate(value, low, high):
    value = max(0, min(1, value))
    return low + (high - low) * value

def crawl_and_convert_to_dataframe(url):
    # Launch web browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    sleep(5) 
    # Wait for the table to be populated
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, '//table//tr')))

    # Find the table element
    table = driver.find_element(By.XPATH,'//table')

    # Extract table data
    data = []
    rows = table.find_elements(By.XPATH, './/tr')
    headers = [cell.text for cell in rows[0].find_elements(By.XPATH, './/td')]
    
    clear_terminal()

    _z = 1
    _last_progress = 0
    len_df = len(rows[1:])
    for row in rows[1:]:  # Skip header row
        progress = floor(interpolate(_z/len_df, 1, 40))
        # progress bar to know when it's done
        if progress != _last_progress:
            clear_terminal()
            print(f"Progress: [{'#'*progress}{'.'*(40-progress)}]")
            _last_progress = progress

        row_data = []
        cells = row.find_elements(By.XPATH, './/td')
        for index, cell in enumerate(cells):
            text = check_background_color(cell)
            text = text.replace('\n', ' = ')
            if index > 3:
                text = add_percentage(text, headers[index])
            row_data.append(text)
        _z += 1
        data.append(row_data)

    driver.quit()

    df = pd.DataFrame(data, columns=headers)
    print('')

    return df 

# URL for bootcamp solve tracker
url = 'https://nsups.github.io/s17'
df = crawl_and_convert_to_dataframe(url)

print(df.head(5))
print('')
filtered_df = df.copy()

# Now we have a dataframe, and we can modify the logic below for data analysis.
# i.e: Get the list of participants who have less than 90% solves in any of the last 4 contests:
THRESHOLD = 90
last_4_columns = df.columns[-4:]

for column in last_4_columns:
    filtered_df[column] = filtered_df[column].str.extract(r'(\d+\.\d+)').astype(float)

# Filtering participants with less than THRESHOLD % in any of the last 4 contests
filtered_participants = filtered_df[(filtered_df[last_4_columns] < THRESHOLD).any(axis=1)]['Participants'].tolist()
print(f"Participants with less than {THRESHOLD}% in any of the last 4 contests: {len(filtered_participants)} people\n")

for p in filtered_participants:
    print(p)
