from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.google.com/search?q=chevron+gas+station+near+Garden+Grove"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
prices = []


petrol_station = soup.find_all("div", attrs={'class': 'VkpGBb'})
for p in petrol_station:
    price = p.find('span', attrs={'class': 'pxqAo iqLmSe OSrXXb Q1JCAd CGu9B'})
    if price is None:
        continue
    station_name = p.find('span', attrs={'class': 'OSrXXb'})
    petrol_type = (price.contents)[0].split("/")[1]
    petrol_type = petrol_type.replace("*", "")
    price = (price.contents)[0].split("/")[0]
    prices.append({'station_name': station_name.contents[0],'gas_type': petrol_type ,'price': price})
print(prices)
