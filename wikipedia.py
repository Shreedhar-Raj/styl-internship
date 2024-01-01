import requests
from bs4 import BeautifulSoup
import csv

def scrape_aephi_chapters(url):
    # Make a request to the Wikipedia page
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the chapter information
        table = soup.find('table', {'class': 'wikitable'})

        # Initialize lists to store active rows of the table
        active_rows = []

        # Iterate over rows in the table
        for row in table.find_all('tr'):
            # Extract data from each column in the row
            columns = row.find_all(['td', 'th'])
            row_data = [column.get_text(strip=True) for column in columns]
            
            # Check if the chapter is marked as "Active" and exclude "Charted" rows
            if len(row_data) >= 4 and row_data[3].lower() == 'active' and 'charted' not in row_data[0].lower():
                active_rows.append(row_data)

        return active_rows
    else:
        # Print an error message if the request was unsuccessful
        print(f"Error: Unable to fetch the page (Status Code {response.status_code})")
        return None

def export_to_csv(data, filename):
    # Write data to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the data
        writer.writerows(data)

# Wikipedia page URL
wikipedia_url = "https://en.wikipedia.org/wiki/List_of_Alpha_Epsilon_Phi_chapters"

# Call the function to scrape chapter information
active_chapters_data = scrape_aephi_chapters(wikipedia_url)

# Specify the CSV file name
csv_filename = "active_aephi_chapters.csv"

# Export data to CSV file
if active_chapters_data:
    export_to_csv(active_chapters_data, csv_filename)
    print(f"Data exported to {csv_filename} successfully.")
else:
    print("No data to export.")
