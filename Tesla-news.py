import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver_path = 'C:\Users\Yao\.cache\selenium\chromedriver\win64\117.0.5938.62'

driver = webdriver.Chrome(chrome_driver_path)


def get_tesla_news():
    driver.get('https://finviz.com/news.ashx')

    search_box = driver.find_element(By.NAME, 's')
    search_box.send_keys('Tesla')

    search_button = driver.find_element(By.NAME, 'SearchTicker')
    search_button.click()

    time.sleep(5)

    news_elements = driver.find_elements(By.CSS_SELECTOR, 'div.news-link-left a')
    news_links = [element.get_attribute('href') for element in news_elements]

    return news_links


def save_to_csv(news_links):
    with open('tesla_news.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])
        for link in news_links:
            writer.writerow([link.text, link.get_attribute('href')])


while True:
    tesla_news = get_tesla_news()

    print("Tesla News Links:")
    for link in tesla_news:
        print(link)

    save_to_csv(tesla_news)
    print("Saved to tesla_news.csv")

    time.sleep(1800)

driver.quit()
