import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
import random

# Load Excel data
input_file = "Affinity_Stock_Generic.xlsx"
output_file = "Updated_Affinity_Stock_Generic.csv"

# Load existing CSV if available, else load from Excel
try:
    data = pd.read_csv(output_file, dtype={'EAN': str})
    print(f"Loaded existing CSV file: {output_file}")
except FileNotFoundError:
    data = pd.read_excel(input_file, engine='openpyxl', dtype={'EAN': str})
    print(f"Loaded Excel file: {input_file}")

# Ensure EANs are properly formatted
data['EAN'] = data['EAN'].str.split('.').str[0]

# Add a column for search numbers if it doesn't exist
if 'search_number' not in data.columns:
    data['search_number'] = ""

# Filter rows where search_number is blank or NA
unprocessed_data = data[(data['search_number'].isna()) | (data['search_number'] == "") | (data['search_number'] == "NA")]

# Exit if no rows need processing
if unprocessed_data.empty:
    print("All rows have been processed. Exiting.")
    exit()

# Create a filtered list of EANs to process
ean_list = unprocessed_data['EAN'].tolist()

# Initialize undetected-chromedriver
driver = uc.Chrome()
wait = WebDriverWait(driver, 10)

# Counter for processed EANs
processed_count = 0

try:
    # Open the Idealo website
    driver.get("https://www.idealo.co.uk/")
    wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # Loop through each EAN number and perform a search
    for index, row in unprocessed_data.iterrows():
        ean = row['EAN']
        print(f"Searching for EAN: {ean}")

        retries = 1
        for attempt in range(retries):
            try:
                # Locate the search bar
                search_bar = driver.find_element(By.NAME, "q")
                search_bar.clear()
                search_bar.send_keys(ean)
                search_bar.send_keys(Keys.RETURN)

                # Wait for results to load
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sr-resultItemLink_YbJS7 a")))

                # Extract the product URL
                product_links = driver.find_elements(By.CSS_SELECTOR, "div.sr-resultItemLink_YbJS7 a")
                product_ids = []
                for link in product_links:
                    href = link.get_attribute("href")
                    match = re.search(r"/compare/(\d+)/", href)
                    if match:
                        product_ids.append(match.group(1))

                if product_ids:
                    extracted_ids = ", ".join(product_ids)
                    data.at[index, 'search_number'] = extracted_ids
                    print(f"Extracted Product IDs: {extracted_ids}")
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for EAN {ean}. Error: {e}")
        else:
            data.at[index, 'search_number'] = "NA"
            print(f"Failed for {ean} after {retries} retries. Assigned 'NA'.")

        # Save progress to CSV after each EAN
        data.to_csv(output_file, index=False)
        print(f"Progress saved for EAN {ean} to {output_file}")

        # Increment the processed counter
        processed_count += 1

        # Add a random delay to mimic human behavior
        time.sleep(random.uniform(5, 10))

        # Add a longer delay every 100 EANs
        if processed_count % 100 == 0:
            print(f"Processed {processed_count} EANs. Adding a longer delay...")
            time.sleep(60)

        # Refresh or navigate back for the next search
        driver.get("https://www.idealo.co.uk/")
        wait.until(EC.presence_of_element_located((By.NAME, "q")))

finally:
    driver.quit()

print("All data fetched and saved to CSV!")
