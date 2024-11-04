from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


soup = BeautifulSoup(driver.page_source, 'html.parser')
prices = []

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

def search_gas_prices():
    driver = init_driver()
    time.sleep(5) #wait for the driver to initialize in case of slow machine
    url = "https://www.google.com/search?q=chevron+gas+station+near+Garden+Grove"
    driver.get(url)
    
    stations = soup.find_all("div", attrs={'class': 'VkpGBb'})
    gas_prices = []
    for station in stations:
        gas_price = station.find('span', attrs={'class': 'pxqAo iqLmSe OSrXXb Q1JCAd CGu9B'})
        if gas_price is None:
            continue
        station_name = station.find('span', attrs={'class': 'OSrXXb'})
        gas_type = (gas_price.contents)[0].split("/")[1]
        gas_type = gas_type.replace("*", "")
        gas_prices.append({'station_name': station_name.contents[0],'gas_type': gas_type ,'price': gas_price})
    
    driver.quit()
    
    return gas_prices

if __name__ == "__main__":
    location = "Garden Grove, CA"
    gas_prices = search_gas_prices()
    
    if gas_prices:
        for station in gas_prices:
            print(station)
    else:
        print({"message": "No gas prices found"})

