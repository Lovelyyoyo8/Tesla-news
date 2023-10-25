import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver_path = 'C:\\Users\\Yao\\.cache\\selenium\\chromedriver\\win64\\117.0.5938.62'

try:
    driver = webdriver.Chrome(chrome_driver_path)
except Exception as e:
    print(f"Error: {e}")
    exit()

def get_tesla_news():
    try:
        driver.get('https://finviz.com/news.ashx')

        search_box = driver.find_element(By.NAME, 's')
        search_box.send_keys('Tesla')

        search_button = driver.find_element(By.NAME, 'SearchTicker')
        search_button.click()

        time.sleep(5)

        news_elements = driver.find_elements(By.CSS_SELECTOR, 'div.news-link-left a')
        news_links = [element.get_attribute('href') for element in news_elements]

        return news_links
    except Exception as e:
        print(f"Error in get_tesla_news: {e}")
        return []

def parse_news_article(url):
    try:
        driver.get(url)
        title = driver.find_element(By.CSS_SELECTOR, 'div.fullview-title').text
        content = driver.find_element(By.CSS_SELECTOR, 'div.fullview-news-outer').text

        return {'title': title, 'content': content}
    except Exception as e:
        print(f"Error in parse_news_article: {e}")
        return {}

def save_to_csv(news_data):
    try:
        with open('tesla_news.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Content'])
            for article in news_data:
                writer.writerow([article['title'], article['content']])
    except Exception as e:
        print(f"Error in save_to_csv: {e}")

try:
    while True:
        tesla_news_links = get_tesla_news()
        news_data = []

        print("Tesla News Links:")
        for link in tesla_news_links:
            print(link)
            news_data.append(parse_news_article(link))

        save_to_csv(news_data)
        print("Saved to tesla_news.csv")

        time.sleep(1800)

except KeyboardInterrupt:
    print("Program terminated by user.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    driver.quit()
