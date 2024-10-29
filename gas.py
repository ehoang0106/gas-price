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
    options.add_argument("--remote-debugging-port=0")  #disable DevTools listening message
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)   
    return driver

def search_gas_prices(location):
    driver = init_driver()
    time.sleep(5) #wait for the driver to initialize in case of slow machine
    
    driver.get("https://www.google.com/maps") #go to google maps
    search_box = driver.find_element(By.NAME, "q") #find the search box
    search_box.send_keys(f"gas stations near {location}") #type in the search box
    search_box.send_keys(Keys.RETURN) #hit enter
    
    time.sleep(10) #wait for the page to load in case of slow internet
    
    gas_prices = [] #gas prices list
    results = driver.find_elements(By.CLASS_NAME, "Nv2PK") #this class is for each gas station result
    
    #loop through each gas station result
    for result in results:
        name = result.find_element(By.CLASS_NAME, "NrDZNb").text #get the name of the gas station
        
        if result.find_elements(By.CLASS_NAME, "ah5Ghc"):
            price = result.find_element(By.CLASS_NAME, "ah5Ghc").text #get the gas price
        else:
            price = "No gas price found."
        
        if not re.search(r'\d+\.\d+', price): #get rid of the station does not has gas price, like costo gas
            price = "No gas price found."
        
        spans = result.find_elements(By.CLASS_NAME, "W4Efsd")
        
        if len(spans) > 2:
            address = spans[2].text
        else:
            address = "No address found."
            
        #remove the unicode character, this is an icon for a wheelchair
        address = address.replace('\ue934', '').strip()
        address = address.replace('Gas station · ', '').strip() # remove the "Gas station · " is a prefix for the address
        
        price = price.replace(' *', '').strip() #remove the * character in price
        gas_prices.append({
            "station_name": name,
            "price": price,
            "address": address
        })
        
    driver.quit() #quit the driver
    
    return gas_prices

if __name__ == "__main__":
    location = "Garden Grove, CA"
    gas_prices = search_gas_prices(location)
    
    if gas_prices:
        print('Results: ')
        for station in gas_prices:
            print(station)
    else:
        print({"message": "No gas prices found."})