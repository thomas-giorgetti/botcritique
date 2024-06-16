import sqlite3
from flask import g
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re

DATABASE = 'db.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS infos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imdbID TEXT UNIQUE,
            title TEXT,
            year TEXT,
            rating INTEGER,
            review TEXT,
            user_id TEXT,
            username TEXT
        )
    ''')
    db.commit()

def parse_imdb_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        final_url = response.url

        if final_url.startswith('http://m.imdb.com'):
            final_url = final_url.replace('http://m.imdb.com', 'https://www.imdb.com')

        response = requests.get(final_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        dom = etree.HTML(str(soup))

        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else 'N/A'

        imdbID = final_url.split('/')[4]

        year = 'N/A'
        
        year_xpaths = [
            "//a[contains(@href, 'releaseinfo')]/text()",
            "//span[@id='titleYear']/a/text()",
            "//div[contains(@class, 'subtext')]/a[last()]/text()"
        ]
        
        for xpath in year_xpaths:
            year_list = dom.xpath(xpath)
            if year_list:
                year_text = year_list[0].strip()
                match = re.search(r'\d{4}', year_text)
                if match:
                    year = match.group(0)
                    break

        if year == 'N/A' and title != 'N/A':
            match = re.search(r'\((\d{4})\)', title)
            if match:
                year = match.group(1)

        original_title = 'N/A'
        
        original_title_xpaths = [
            "//div[contains(@class, 'originalTitle')]/text()",
            "//div[@data-testid='hero-title-block__original-title']/text()"
        ]
        
        for xpath in original_title_xpaths:
            original_title_list = dom.xpath(xpath)
            if original_title_list:
                original_title = original_title_list[0].strip()
                break

        return {
            'imdbID': imdbID,
            'title': title,
            'year': year,
            'original_title': original_title
        }
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page: {e}")
        return None
