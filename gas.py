from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import boto3
from time import strftime
import pytz
from datetime import datetime

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

def insert_into_dynamodb(date, station_name, price_value, price_type, address):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('GasPricesTracker')
    
    response = table.put_item(
        Item={
            'date': date,
            'station_name': station_name,
            'price': price_value,
            'price_type': price_type,
            'address': address
        }
    )
    return response
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
        #get the name of the gas station
        name = result.find_element(By.CLASS_NAME, "NrDZNb").text 
        
        #get the gas price
        
        price_element = result.find_element(By.CLASS_NAME, "ah5Ghc")
        price = price_element.text if price_element else ""
        
        #remove stations without gas prices
        if not re.search(r'\d+\.\d+', price):
            continue
        else:
            price = price.replace(' *', '')
        
        #split the price into value and type
        price_value, price_type = (price.split('/') + [""])[:2]
        
        
        #get the address of the gas station
        spans = result.find_elements(By.CLASS_NAME, "W4Efsd")
        if len(spans) > 2:
            address = spans[2].text
        else:
            continue
        
        #remove the wheelchair icon from the address, remove Gas station · and ·
        address = address.replace('\ue934', '').replace('Gas station · ', '').replace('· ', '').strip() 
        date = datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d %H:%M:%S")
        
        #append to the list to print out the result later
        gas_prices.append({
            "date": date,
            "station_name": name,
            "price": price_value,
            "price_type": price_type,
            "address": address
        })
        
        #insert into DynamoDB
        insert_into_dynamodb(date, name, price_value, price_type, address)
        time.sleep(5) #wait for 1 second before moving to the next gas station to avoid bottle neck on the database
        
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