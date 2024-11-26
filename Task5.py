import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the e-commerce site
baseurl = "https://www.thewhiskyexchange.com"
headers = {'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def get_product_links():
    """Fetch product links from the main page."""
    product_links = []
    for x in range(1, 6):  # Scraping first 5 pages
        url = f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}&psize=24&sort=pasc'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        productlist = soup.find_all("li", {"class": "product-grid__item"})
        
        for product in productlist:
            link = product.find("a", {"class": "product-card"}).get('href')
            product_links.append(baseurl + link)
    
    return product_links

def scrape_product_data(product_links):
    """Scrape product data from each product page."""
    data = []
    
    for link in product_links:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            name = soup.find("h1", {"class": "product-main__name"}).text.strip()
        except:
            name = None
        
        try:
            price = soup.find("p", {"class": "product-action__price"}).text.strip()
        except:
            price = None
        
        try:
            rating = soup.find("div", {"class": "review-overview"}).text.strip()
        except:
            rating = None
        
        product_info = {"name": name, "price": price, "rating": rating}
        data.append(product_info)
    
    return data

def save_to_csv(data):
    """Save the scraped data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv('product_data.csv', index=False)

def main():
    product_links = get_product_links()
    product_data = scrape_product_data(product_links)
    save_to_csv(product_data)
    print("Data has been scraped and saved to product_data.csv")

if __name__ == "__main__":
    main()