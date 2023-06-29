import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Google search query
query = 'site:youtube.com openinapp.co'

# Number of results to scrape
num_results = 35
c = 0
# Store the YouTube channel links
channel_links = []

# Configure Chrome options
chrome_options = Options()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
query = f'https://www.google.com/search?q={query}'
# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Perform the Google search
driver.get(query)
time.sleep(1)

while len(channel_links) < num_results:
    # Collect the visible search results
    results = driver.find_elements(By.XPATH, '//div[@id="search"]//a')
    urls = [result.get_attribute('href') for result in results]
    urls = urls[0::3]

    try:
        # Find the channel link on the video page
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'pnnext'))
        )

        # Get the href attribute value
        query = element.get_attribute('href')
        query = query

    except:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'YMLwIe'))
        )

        # Get the href attribute value
        query = element.get_attribute('href')
        query = query
        print(query)
        pass

    for url in urls:
        if 'youtube.com/channel/' in url:
            channel_links.append(url)

        if len(channel_links) >= num_results:
            break
        if 'youtube.com/watch' or 'google.com/search' in url:
            driver.get(url)
            time.sleep(1)
            try:
                # Find the channel link on the video page
                channel_link_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="channel-name"]')))

                channel_name = channel_link_element.text
                c+=1

                print(channel_name, f"---{c}")
                channel_links.append(f'https://www.youtube.com/{channel_name}')


            except:
                pass
            # Wait for the video page to load'''

    # Check if we have collected enough results
    if len(channel_links) >= num_results:
        break
    driver.get(query)

    time.sleep(1)  # Wait for the page to load more results

# Close the browser
driver.quit()

# Save the results in CSV format
with open('youtube_channels.csv', 'w', newline='',encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['YouTube Channel Links'])
    writer.writerows([[link] for link in channel_links])