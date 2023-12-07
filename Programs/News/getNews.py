import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import logging

with open("D:/MarketMasterAI/Def/Path.json", 'r') as file:
    data = json.load(file)
    json_file = data['json_paths']['News']
    log = data["log_paths"]["getNews"]

logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_page_content(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.error(f"Error fetching {url}: HTTP status {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

async def extract_text_from_paragraphs(session, url):
    html = await fetch_page_content(session, url)
    if html:
        try:
            soup = BeautifulSoup(html, 'html.parser')
            p_tags = soup.find_all('p')
            return ' '.join(tag.get_text(strip=True) for tag in p_tags)
        except Exception as e:
            logging.error(f"Error parsing HTML from {url}: {e}")
            return None
    else:
        return None

async def get_article_contents(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [extract_text_from_paragraphs(session, url) for url in urls]
        return await asyncio.gather(*tasks)

def initialize_web_driver():
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument('--log-level=3')
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
        driver.implicitly_wait(3)
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        return None

def fetch_trending_articles_urls(driver):
    try:
        driver.get("https://coinpost.jp/")
        trending_articles = []

        for i in range(1, 6):
            link = driver.find_element(By.XPATH,f"/html/body/div[1]/div[4]/div/div[1]/div[2]/div/div/div/div[{i}]/a").get_attribute("href")
            title = driver.find_element(By.XPATH,f"/html/body/div[1]/div[4]/div/div[1]/div[2]/div/div/div/div[{i}]/a/span[2]").text
            trending_articles.append({"title": title, "link": link})

        return trending_articles
    except Exception as e:
        logging.error(f"Error fetching trending article URLs: {e}")
        return []
    finally:
        driver.quit()

async def main():
    driver = initialize_web_driver()
    if driver:
        trending_articles = fetch_trending_articles_urls(driver)
        if trending_articles:
            urls = [article['link'] for article in trending_articles]
            articles_content = await get_article_contents(urls)

            for article, content in zip(trending_articles, articles_content):
                article['content'] = content if content else "Content not available"

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(trending_articles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
