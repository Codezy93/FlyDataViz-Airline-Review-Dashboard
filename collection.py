import requests
from bs4 import BeautifulSoup
from urllib3 import request
import pandas as pd

def collection(name, pages):
    retdict = {}
    reviews = []
    stars = []
    date = []
    country = []
    
    # Collect data from each page
    for i in range(1, pages + 1):
        page = requests.get(f"https://www.airlinequality.com/airline-reviews/{name}/page/{i}/?sortby=post_date%3ADesc&pagesize=100")
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Extract reviews
        for item in soup.find_all("div", class_="text_content"):
            reviews.append(item.text.strip())
        
        # Extract star ratings
        for item in soup.find_all("div", class_="rating-10"):
            try:
                stars.append(item.span.text.strip())
            except AttributeError:
                print(f"Error on page {i}")
        
        # Extract review dates
        for item in soup.find_all("time"):
            date.append(item.text.strip())
        
        # Extract countries
        for item in soup.find_all("h3"):
            try:
                country.append(item.span.next_sibling.text.strip(" ()"))
            except AttributeError:
                country.append('Unknown')
    
    # Ensure the length of stars matches reviews
    stars = stars[:len(reviews)]
    
    # Create DataFrame from collected data
    df = pd.DataFrame({
        "reviews": reviews,
        "stars": stars,
        "date": date,
        "country": country
    })

    # Save DataFrame to CSV
    df.to_csv(f"{name}_reviews.csv", index=False)

    return f"Data collected and saved to {name}_reviews.csv"

site_id = "air-india"
pages = 10

collection(site_id, pages)