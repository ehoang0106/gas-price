from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import boto3
import re
from datetime import datetime
import pytz

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

def insert_into_dynamodb(date, station_name, price, gas_type, address):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('GasPricesTracking')
    
    response = table.put_item(
        Item={
            'date': date,
            'station_name': station_name,
            'price': price,
            'gas_type': gas_type,
            'address': address
        }
    )
    return response

def search_gas_prices(location):
    driver = init_driver()
    time.sleep(5) #wait for the driver to initialize in case of slow machine
    formatted_location = location.replace(" ", "+")
    url = f"https://www.google.com/search?q=chevron+gas+station+near+{formatted_location}"
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stations = soup.find_all("div", attrs={'class': 'VkpGBb'})
    gas_prices = []
    lowest_price = []
    for station in stations:
        gas_price = station.find('span', attrs={'class': 'pxqAo iqLmSe OSrXXb Q1JCAd CGu9B'})
        if gas_price is None:
            continue
        station_name = station.find('span', attrs={'class': 'OSrXXb'}).get_text()
        
        #address
        address_div = station.find('div', attrs={'class': 'rllt__details'})
        if address_div:
            address = address_div.contents[1].get_text()
        else:
            address = "Address not found"
        #remove the dot character and phone number of the station
        address = re.sub(r' · \(\d{3}\) \d{3}-\d{4}', '', address)
        
        
        gas_type = (gas_price.contents)[0].split("/")[1]
        gas_type = gas_type.replace("*", "")
        price = (gas_price.contents)[0].split("/")[0]
        price_value = float(price.replace("$", ""))
        
        
        gas_prices.append({'station_name': station_name,'gas_type': gas_type ,'price': price,'price_value': price_value, 'address': address})
        lowest_price.append(price_value);
        
        min_price = min(lowest_price);
        if price_value == min_price:
            lowest_price_station = {'station_name': station_name,'gas_type': gas_type ,'price': price,'price_value': price,'address': address}
        
        date = datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d %H:%M:%S")
        
        
        #insert into DynamoDB
        insert_into_dynamodb(date, station_name, price, gas_type, address)
        time.sleep(2) #wait for 1 second before moving to the next gas station to avoid bottle neck on the database
        
    driver.quit()
    
    
    
    return gas_prices, lowest_price_station

if __name__ == "__main__":
    location = "Garden Grove, CA"
    gas_prices, lowest_price_station = search_gas_prices(location)
    
    if gas_prices:
        for station in gas_prices:
            print(station)
    else:
        print({"message": "No gas prices found"})
    
    print(type(gas_prices))
    
    print("Lowest price station: ")
    print(lowest_price_station)
    print(type(lowest_price_station))