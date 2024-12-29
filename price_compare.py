from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")

driver_path = "chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

input_file = "updated_file.csv"
data = pd.read_csv(input_file)

output_file = "output.csv"

with open(output_file, "w", encoding="utf-8") as f:  # Ensure UTF-8 encoding
    f.write("search_number,shop_name,price,product_link\n")

for _, row in data.iterrows():
    search_number = row["search_number"]
    url = f"https://www.idealo.co.uk/compare/{search_number}"
    
    try:
        driver.get(url)
        driver.implicitly_wait(10)

        offer_items = driver.find_elements(By.CSS_SELECTOR, "li.productOffers-listItem")
        
        for item in offer_items:
            try:
 
                shop_name = item.get_attribute("data-mtrx-click")
                shop_name = shop_name.split('"shop_name":"')[1].split('"')[0] if shop_name else "N/A"

                # Extract price
                price_element = item.find_element(By.CSS_SELECTOR, ".productOffers-listItemOfferPrice")
                price = price_element.text.strip().replace("\n", " ") if price_element else "N/A"

                # Extract product link
                link_element = item.find_element(By.CSS_SELECTOR, "a.productOffers-listItemTitle")
                product_link = link_element.get_attribute("href") if link_element else "N/A"

                # Append to results incrementally
                with open(output_file, "a", encoding="utf-8") as f:  # Use UTF-8 encoding
                    f.write(f"{search_number},{shop_name},{price},{product_link}\n")
            except Exception as e:
                print(f"Error extracting item: {e}")

    except Exception as e:
        print(f"Error processing {url}: {e}")

# Close the driver
driver.quit()

print(f"Data saved incrementally to {output_file}")
