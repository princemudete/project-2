import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import datetime

# Logging setup
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_jobs():
    print("Starting scraping process...")
    url = "https://vacancymail.co.zw/jobs/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises error for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        job_cards = soup.select(".job-listing")
        if not job_cards:
            print("No job listings found.")
            return

        job_data = []

        for job in job_cards:
            title = job.select_one(".job-listing-title").text.strip() if job.select_one(".job-listing-title") else "N/A"
            company = job.select_one(".job-listing-company").text.strip() if job.select_one(".job-listing-company") else "N/A"
            
            location = job.select_one(".icon-material-outline-location-on")
            location_text = location.find_next('li').text.strip() if location else "N/A"
            
            expiry = job.select_one(".icon-material-outline-access-time")
            expiry_text = expiry.find_next('li').text.strip() if expiry else "N/A"
            
            description = job.select_one(".job-listing-text").text.strip() if job.select_one(".job-listing-text") else "N/A"

            job_data.append({
                "Title": title,
                "Company": company,
                "Location": location_text,
                "Expiry Date": expiry_text,
                "Description": description
            })

        df = pd.DataFrame(job_data)
        df.drop_duplicates(inplace=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"scraped_data_{timestamp}.csv"
        df.to_csv(file_name, index=False)

        print(f"✅ Scraping completed! Data saved to {file_name}")
        logging.info("Scraping completed successfully.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        print(f"Request error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

# ✅ Correct main check
if __name__ == "__main__":
    scrape_jobs()


