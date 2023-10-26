import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

chrome_driver_path = 'C:\Users\Yao\.cache\selenium\chromedriver\win64\117.0.5938.62'

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


class TestTeslaNewsScraper(unittest.TestCase):
    def test_get_tesla_news(self):
        news_links = get_tesla_news()
        self.assertIsInstance(news_links, list)
        self.assertTrue(all(isinstance(link, str) for link in news_links))

    def test_parse_news_article(self):
        url = 'https://example.com/news_article'
        news_data = parse_news_article(url)
        self.assertIsInstance(news_data, dict)
        self.assertIn('title', news_data)
        self.assertIn('content', news_data)
        self.assertIsInstance(news_data['title'], str)
        self.assertIsInstance(news_data['content'], str)

    def test_save_to_csv(self):
        test_data = [{'title': 'Test Title 1', 'content': 'Test Content 1'},
                     {'title': 'Test Title 2', 'content': 'Test Content 2'}]

        save_to_csv(test_data)

        import os
        self.assertTrue(os.path.isfile('tesla_news.csv'))

        with open('tesla_news.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(header, ['Title', 'Content'])

            row1 = next(reader)
            self.assertEqual(row1, ['Test Title 1', 'Test Content 1'])

            row2 = next(reader)
            self.assertEqual(row2, ['Test Title 2', 'Test Content 2'])

if __name__ == '__main__':
    unittest.main()

driver.quit()
