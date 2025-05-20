import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

PROPERTY_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf9wZwxWePdvbJDo-pqLCgB5oMQ4XWn1A3yQiejW3IBnCv_nA/viewform?usp=dialog"

def get_property_data(url):
    """Scrape data from the url"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        web_page = response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to retrieve property data: {e}")
        return [], [], []

    soup = BeautifulSoup(web_page, "html.parser")
    addresses_from_web = soup.find_all('address', {'data-test': 'property-card-addr'})
    prices_from_web = soup.find_all('span' ,class_="PropertyCardWrapper__StyledPriceLine")
    links_from_web = soup.find_all('div', {'class': 'StyledPropertyCardDataWrapper'})

    address_list = [address.getText(strip=True) for address in addresses_from_web]
    prices_list = [price.getText(strip=True).strip("+/mo 1bd") for price in prices_from_web]
    links_list = [link.find('a', href=True)['href'] for link in links_from_web if link.find('a', href=True)]

    return address_list, prices_list, links_list

def setup_browser():
    """Set up and return a Chrome WebDriver instance."""
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)
    except Exception as e:
        print(f"[ERROR] Failed to launch Chrome WebDriver: {e}")
        raise

def fill_form(driver, form_url, addresses, prices, links):
    """Open the form and submit the data."""
    time.sleep(2)
    for i in range(len(addresses)):
        try:
            driver.get(form_url)
            time.sleep(2)
            input_fields = driver.find_elements(By.CSS_SELECTOR, 'input.whsOnd[jsname="YPqjbf"]')

            input_fields[0].send_keys(addresses[i])
            input_fields[1].send_keys(prices[i])
            input_fields[2].send_keys(links[i])

            submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_button.click()
            # time.sleep(2)
            # next_form = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]')
            # next_form.click()
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Failed to submit form for {addresses[i]}: {e}")

def main():
    addresses, prices, links = get_property_data(PROPERTY_URL)
    driver = setup_browser()
    fill_form(driver, FORM_URL, addresses, prices, links)

main()