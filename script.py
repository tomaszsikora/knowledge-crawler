from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=~/Library/Application Support/Google/Chrome/Default")
    service = Service('/usr/local/bin/chromedriver')
    return webdriver.Chrome(service=service, options=chrome_options)

def login(driver, login_url):
    driver.get(login_url)
    input("Please log in manually and press Enter when done...")

def crawl_articles(driver, start_url, output_file):
    driver.get(start_url)

    # You may need to implement logic to navigate through pages or find article links
    article_links = driver.find_elements(By.CSS_SELECTOR, '.devsite-nav-title')

    with open(output_file, 'w', encoding='utf-8') as f:
        for link in article_links:
            url = link.get_attribute('href')
            driver.get(url)

            # Wait for the content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.devsite-article'))
            )

            # Extract the rendered content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            content = soup.select_one('.devsite-article').get_text(strip=True)

            article = {
                'url': url,
                'content': content
            }

            # Write the article as a single JSON line
            f.write(json.dumps(article, ensure_ascii=False) + '\n')

            time.sleep(1)  # Be respectful to the server

def main():
    login_url = "https://bazel.build/run/build"
    start_url = "https://bazel.build/run/build"
    output_file = "knowledge_base_articles.jsonl"

    driver = setup_driver()
    login(driver, login_url)
    crawl_articles(driver, start_url, output_file)
    driver.quit()

if __name__ == "__main__":
    main()