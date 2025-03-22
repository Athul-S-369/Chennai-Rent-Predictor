from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os
import concurrent.futures
import requests
from functools import lru_cache
from datetime import datetime, timedelta

# Dictionary of supported locations in Chennai with their encoding
LOCATIONS = {
    'Anna Nagar': 1,
    'T Nagar': 2,
    'Velachery': 3,
    'Adyar': 4,
    'Nungambakkam': 5,
    'Kilpauk': 6,
    'Kodambakkam': 7,
    'Royapettah': 8,
    'Saidapet': 9,
    'Medavakkam': 10,
    'Pallavaram': 11,
    'Chromepet': 12,
    'Guindy': 13,
    'Egmore': 14,
    'Perungudi': 15,
    'Sholinganallur': 16
}

# Cache for storing scraped data
CACHE_FILE = 'data/rental_cache.json'
CACHE_DURATION = timedelta(hours=24)  # Cache duration in hours

def is_cache_valid():
    try:
        if not os.path.exists(CACHE_FILE):
            return False
        cache_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        return datetime.now() - cache_time < CACHE_DURATION
    except:
        return False

@lru_cache(maxsize=100)
def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except:
        return None

def setup_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        
        service = Service()
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.set_page_load_timeout(10)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        return None

def extract_rental_data_from_html(html_content):
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    property_cards = soup.find_all('div', class_='property-card')
    
    rental_data = []
    for card in property_cards:
        try:
            # Extract all data at once to reduce DOM queries
            location = card.find('div', class_='property-location').text.strip()
            area_text = card.find('div', class_='property-area').text.strip()
            rent_text = card.find('div', class_='property-rent').text.strip()
            beds_text = card.find('div', class_='property-beds').text.strip()
            
            # Process the extracted data
            area = float(area_text.split()[0])
            rent = float(rent_text.replace('₹', '').replace(',', ''))
            bedrooms = int(beds_text.split()[0])
            
            rental_data.append({
                'location': location,
                'area': area,
                'rent': rent,
                'bedrooms': bedrooms
            })
        except Exception as e:
            continue
    
    return rental_data

def scrape_page(page_num):
    url = f"https://www.99acres.com/rent-property-in-chennai?page={page_num}"
    print(f"Scraping page {page_num}...")
    
    # Try using requests first (faster)
    html_content = get_page_content(url)
    if html_content:
        return extract_rental_data_from_html(html_content)
    
    # Fallback to Selenium if requests fails
    driver = setup_driver()
    if not driver:
        return []
    
    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "property-card"))
        )
        return extract_rental_data_from_html(driver.page_source)
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def scrape_rental_data():
    # Check cache first
    if is_cache_valid():
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Use ThreadPoolExecutor for concurrent scraping
    rental_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_page = {executor.submit(scrape_page, page): page for page in range(1, 6)}
        
        for future in concurrent.futures.as_completed(future_to_page):
            page_data = future.result()
            rental_data.extend(page_data)
    
    # Save to cache
    os.makedirs('data', exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(rental_data, f)
    
    return rental_data

def save_rental_data(data):
    os.makedirs('data', exist_ok=True)
    
    # Save as JSON
    with open('data/rental_data.json', 'w') as f:
        json.dump(data, f)
    
    # Save as CSV
    df = pd.DataFrame(data)
    df.to_csv('data/rental_data.csv', index=False)

def load_rental_data():
    try:
        # Try to load from JSON first
        with open('data/rental_data.json', 'r') as f:
            return json.load(f)
    except:
        try:
            # Try to load from CSV
            return pd.read_csv('data/rental_data.csv').to_dict('records')
        except:
            return []

if __name__ == "__main__":
    # Scrape new data
    rental_data = scrape_rental_data()
    print(f"Scraped {len(rental_data)} rental listings") 