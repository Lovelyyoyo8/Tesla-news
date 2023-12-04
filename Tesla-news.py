import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

chrome_driver_path = 'C:\\Users\\Yao\\.cache\\selenium\\chromedriver\\win64\\117.0.5938.62'

try:
    driver = webdriver.Chrome(chrome_driver_path)
    print('Chrome driver initialized successfully.')
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    exit()

def get_tesla_news():
    try:
        driver.get('https://finviz.com/news.ashx')
        print('Opened the Tesla news page.')

        search_box = driver.find_element(By.NAME, 's')
        search_box.send_keys('Tesla')
        print('Entered "Tesla" into the search box.')

        search_button = driver.find_element(By.NAME, 'SearchTicker')
        search_button.click()
        print('Clicked the search button.')

        wait = WebDriverWait(driver, 10)
        # Wait for the news links to load dynamically
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.news-link-left a')))
        print('Waited for news links to load dynamically.')

        news_elements = driver.find_elements(By.CSS_SELECTOR, 'div.news-link-left a')
        news_links = [element.get_attribute('href') for element in news_elements]

        return news_links
    except Exception as e:
        print(f"Error in get_tesla_news: {e}")
        return []

def parse_news_article(url):
    try:
        driver.get(url)
        print(f'Opened the news article: {url}')

        title = driver.find_element(By.CSS_SELECTOR, 'div.fullview-title').text
        content = driver.find_element(By.CSS_SELECTOR, 'div.fullview-news-outer').text

        return {'title': title, 'content': content}
    except Exception as e:
        print(f"Error in parse_news_article: {e}")
        return {}

def save_to_csv(news_data):
    try:
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = f'tesla_news_{timestamp}.csv'
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Content'])
            for article in news_data:
                writer.writerow([article['title'], article['content']])
        print(f'Saved data to CSV file: {filename}')
    except Exception as e:
        print(f"Error in save_to_csv: {e}")

class TestTeslaNewsScraper(unittest.TestCase):
    def test_get_tesla_news(self):
        news_links = get_tesla_news()
        self.assertIsInstance(news_links, list)
        self.assertTrue(all(isinstance(link, str) for link in news_links))
        print('Test for get_tesla_news passed.')

    def test_parse_news_article(self):
        url = 'https://example.com/news_article'
        news_data = parse_news_article(url)
        self.assertIsInstance(news_data, dict)
        self.assertIn('title', news_data)
        self.assertIn('content', news_data)
        self.assertIsInstance(news_data['title'], str)
        self.assertIsInstance(news_data['content'], str)
        print('Test for parse_news_article passed.')

    def test_save_to_csv(self):
        test_data = [{'title': 'Test Title 1', 'content': 'Test Content 1'},
                     {'title': 'Test Title 2', 'content': 'Test Content 2'}]

        save_to_csv(test_data)

        import os
        self.assertTrue(os.path.isfile('tesla_news.csv'))
        print('Test for save_to_csv passed.')

        with open('tesla_news.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(header, ['Title', 'Content'])

            row1 = next(reader)
            self.assertEqual(row1, ['Test Title 1', 'Test Content 1'])

            row2 = next(reader)
            self.assertEqual(row2, ['Test Title 2', 'Test Content 2'])

if __name__ == '__main__':
    try:
        unittest.main()
        print('All tests passed successfully.')
    except Exception as e:
        print(f"Error in running tests: {e}")
    finally:
        driver.quit()
        print('Chrome driver quit.')
