from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def search_gas_prices(location):
    driver = init_driver()
    
    driver.get("https://www.google.com/maps")
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"gas stations near {location}")
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(10)
    
    gas_prices = []
    results = driver.find_elements(By.CLASS_NAME, "Nv2PK")
    for result in results:
        name = result.find_element(By.CLASS_NAME, "NrDZNb").text
        price = result.find_element(By.CLASS_NAME, "ah5Ghc").text if result.find_elements(By.CLASS_NAME, "ah5Ghc") else "No gas price found."
        
        if not re.search(r'\d+\.\d+', price): #get rid of the station does not has gas price, like costo gas
            price = "No gas price found."
        
        spans = result.find_elements(By.CLASS_NAME, "W4Efsd")
        address = spans[2].text if len(spans) > 2 else "No address found."
        
        address = address.replace('\ue934', '').strip() #remove the unicode character, this is an icon for a wheelchair 
        
        gas_prices.append({
            "station_name": name,
            "price": price,
            "address": address
        })
    
    driver.quit()
    
    return gas_prices

if __name__ == "__main__":
    location = "Garden Grove, CA"
    gas_prices = search_gas_prices(location)
    
    if gas_prices:
        print("Gas prices near", location)
        for station in gas_prices:
            print(station)
    else:
        print({"message": "No gas prices found."})
