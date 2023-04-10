from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

GOOGLE_FORM_LINK = "https://forms.gle/jpQkJ53enZHGRPKj8"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
              "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
              "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C" \
              "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
              "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
              "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A" \
              "%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse" \
              "%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B" \
              "%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
                  "Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,nl;q=0.8"
}

data = requests.get(ZILLOW_LINK, headers=header)
soup = BeautifulSoup(data.text, "html.parser")

listing = []

pages = soup.find("span", attrs={"class": "result-count"}).text
new_pages = pages.split(" ")[0].replace(",", "")
amount_of_pages = int((int(new_pages) / 50))
print(amount_of_pages)

for n in range(amount_of_pages):
    n += 1
    ZILLOW_LINK_iterate = f"https://www.zillow.com/homes/for_rent/9_p/?searchQueryState=%7B%22mapBounds%22%3A%7B" \
                          f"%22west%22%3A-122.6424125571289%2C%22east%22%3A-122.2242454428711%2C%22south%22%3A37" \
                          f".548895800417334%2C%22north%22%3A38.0009959434336%7D%2C%22mapZoom%22%3A11%2C" \
                          f"%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D" \
                          f"%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22" \
                          f"%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B" \
                          f"%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value" \
                          f"%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22" \
                          f"%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22pagination%22%3A%7B%22currentPage%22%3A" \
                          f"{n}%7D%7D"
    data = requests.get(ZILLOW_LINK_iterate, headers=header)
    soup = BeautifulSoup(data.text, "html.parser")
    ul_list_finding = soup.find("ul", class_="List-c11n-8-85-1__sc-1smrmqp-0")
    try:
        for item in ul_list_finding:
            if item.address:
                price = item.find("span", attrs={"data-test": "property-card-price"}).text
                actual_price = price.split("/")[0]
                listing.append({
                    "address": item.address.text,
                    "link": item.a["href"],
                    "price": actual_price
                })
    finally:
        pass

# print(listing)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for item in listing:
    driver.get(GOOGLE_FORM_LINK)
    time.sleep(2)
    answer_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                   '2]/div/div[1]/div/div[1]/input')
    answer_address.send_keys(item["address"])
    answer_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                                 '1]/div/div[1]/input')
    answer_price.send_keys(item["price"])
    answer_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                                '1]/div/div[1]/input')
    answer_link.send_keys(item["link"])
    send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    send_button.click()

spreadsheet_link = 'https://docs.google.com/forms/d/1_3-TV8jgl2lTwzvrWRlvAh6GeH1YUNxtMKNQ_PsaWmE/edit#responses'

driver.get(spreadsheet_link)
time.sleep(2)
spreadsheet = driver.find_element(By.XPATH,
                                  '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/span[2]')
spreadsheet.click()
time.sleep(200)
