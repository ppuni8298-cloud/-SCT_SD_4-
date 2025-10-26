import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Example URL — replace with your target site (must allow scraping)
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Data lists
product_names = []
product_prices = []
product_ratings = []

# Loop through multiple pages (example: 5 pages)
for page in range(1, 6):
    print(f"Scraping page {page}...")
    url = BASE_URL.format(page)
    response = requests.get(url)
    response.raise_for_status()  # check for HTTP errors
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract product containers
    products = soup.find_all("article", class_="product_pod")
    
    for product in products:
        # Product name
        name = product.h3.a["title"]
        
        # Product price
        price = product.find("p", class_="price_color").text.strip()
        
        # Product rating (class name like "star-rating Three")
        rating_class = product.p["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "No rating"
        
        # Store data
        product_names.append(name)
        product_prices.append(price)
        product_ratings.append(rating)
    
    # Optional delay to avoid overloading the site
    time.sleep(1)

# Create DataFrame
data = pd.DataFrame({
    "Product Name": product_names,
    "Price": product_prices,
    "Rating": product_ratings
})

# Save to CSV
data.to_csv("products.csv", index=False)
print("✅ Data saved to products.csv")
