from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://www.google.com/search?q=gas+station+garden+grove+&sca_esv=2e8d468bbac54b5e&sxsrf=ADLYWIKi-F3IeTHK8zKlCRjO_tSVD0Mi0g%3A1730090868013&ei=dBcfZ4JBwNiQ8g_U863ICQ&ved=0ahUKEwiCy_fcorCJAxVALEQIHdR5C5kQ4dUDCBA&uact=5&oq=gas+station+garden+grove+&gs_lp=Egxnd3Mtd2l6LXNlcnAiGWdhcyBzdGF0aW9uIGdhcmRlbiBncm92ZSAyBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkiOHlDZDVjcG3ABeAGQAQCYAUugAYIHqgECMTW4AQPIAQD4AQGYAhCgArkHwgIKEAAYsAMY1gQYR8ICEBAAGIAEGLADGEMYyQMYigXCAhkQLhiABBiwAxjRAxhDGMcBGMgDGIoF2AEBwgIKECMYgAQYJxiKBcICCxAAGIAEGJIDGIoFwgINEAAYgAQYsQMYFBiHAsICBRAAGIAEwgILEAAYgAQYkQIYigXCAgoQABiABBgUGIcCmAMAiAYBkAYLugYECAEYCJIHAjE2oAfSYw&sclient=gws-wiz-serp"

driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
prices = []


with open('out.html', "w", encoding="utf-8") as file:
    file.write(driver.page_source)

petrol_station = soup.find_all("div", attrs={'class': 'gEJ7Ib FyvIhd'})
for p in petrol_station:
    price = p.find('span', attrs={'class': 'pxqAo iqLmSe OSrXXb Q1JCAd CGu9B'})
    if price is None:
        continue
    station_name = p.find('span', attrs={'class': 'OSrXXb'})
    petrol_type = (price.contents)[0].split("/")[1]
    petrol_type = petrol_type.replace("*", "")
    price = (price.contents)[0].split("/")[0]
    prices.append({'station_name': station_name.contents[0],'petrol_type': petrol_type ,'price': price})
print(prices)