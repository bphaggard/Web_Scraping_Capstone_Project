import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

PROPERTY_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf9wZwxWePdvbJDo-pqLCgB5oMQ4XWn1A3yQiejW3IBnCv_nA/viewform?usp=dialog"

response = requests.get(PROPERTY_URL)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
addresses_from_web = soup.find_all('address', {'data-test': 'property-card-addr'})
prices_from_web = soup.find_all('span' ,class_="PropertyCardWrapper__StyledPriceLine")
links_from_web = soup.find_all('div', {'class': 'StyledPropertyCardDataWrapper'})

address_list = [address.getText(strip=True) for address in addresses_from_web]
prices_list = [price.getText(strip=True).strip("+/mo 1bd") for price in prices_from_web]
links_list = [link.find('a', href=True)['href'] for link in links_from_web if link.find('a', href=True)]

# Keep Chrome browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)


time.sleep(2)
# Filling forms
for i in range(len(address_list)):
    driver.get(FORM_URL)
    time.sleep(2)
    input_fields = driver.find_elements(By.CSS_SELECTOR, 'input.whsOnd[jsname="YPqjbf"]')

    input_fields[0].send_keys(address_list[i])
    input_fields[1].send_keys(prices_list[i])
    input_fields[2].send_keys(links_list[i])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()
    # time.sleep(2)
    # next_form = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]')
    # next_form.click()
    time.sleep(2)
