from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    wait = WebDriverWait(driver, 20)  
  
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(f"gas stations near {location}")
        search_box.send_keys(Keys.RETURN)
    except Exception as e:
        print("Failed to find search box:", e)
        driver.quit()
        return []
    
    time.sleep(10) 
    
    gas_prices = []
    try:
        results = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Nv2PK")))
        for result in results:
            try:
                name = result.find_element(By.CLASS_NAME, "NrDZNb").text 
                try:
                    price = result.find_element(By.CLASS_NAME, "ah5Ghc").text 
            
                    if not re.search(r'\d+\.\d+', price):
                        price = "No gas price found."
                except:
                    price = "No gas price found."
                
                spans = result.find_elements(By.CLASS_NAME, "W4Efsd")
                address = spans[2].text if len(spans) > 2 else "No address found."  
                
                address = address.replace('\ue934', '').strip()  
                
                gas_prices.append({
                    "station_name": name,
                    "price": price,
                    "address": address
                })
            except Exception as e:
                print("Could not extract information:", e)
                continue
    except Exception as e:
        print("Error fetching results:", e)
    
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
