import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.existing_data = set()

    def extract_headings(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            main_headings = soup.find_all('h1')
            all_data = []
            for main_heading in main_headings:
                main_heading_text = main_heading.text.strip()
                subheadings = main_heading.find_all_next(['h2', 'h3', 'h4', 'h5', 'h6'])
                subheadings_text = ", ".join(subheading.text.strip() for subheading in subheadings)
                Codesnippet = main_heading.find_next('pre')
                unix_macos_code = Codesnippet.text.strip() if Codesnippet else None
                data = (main_heading_text, subheadings_text, unix_macos_code)
                if data not in self.existing_data:
                    all_data.append(data)
                    self.existing_data.add(data)

            links = soup.find_all('a', href=True)
            for link in links:
                link_url = urljoin(self.url, link['href'])
                data = self.extract_data_from_page(link_url)
                if data:
                    all_data.extend(data)
            return all_data
        else:
            print("Failed to retrieve data from the URL.")
            return None

    def extract_data_from_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            Codesnippet = soup.find('pre')
            unix_macos_code = Codesnippet.text.strip() if Codesnippet else None
            main_headings = soup.find_all('h1')
            data_list = []
            for main_heading in main_headings:
                main_heading_text = main_heading.text.strip()
                subheadings = main_heading.find_all_next(['h2', 'h3', 'h4', 'h5', 'h6'])
                subheadings_text = ", ".join(subheading.text.strip() for subheading in subheadings)
                data = (main_heading_text, subheadings_text, unix_macos_code)
                if data not in self.existing_data:
                    data_list.append(data)
                    self.existing_data.add(data)
            return data_list
        else:
            print(f"Failed to retrieve data from the linked page: {url}")
            return None

    def write_to_csv(self, data, filename):
        if data:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Headings", "Subheadings", "Code Snippets"])
                for row in data:
                    writer.writerow(row)
            print(f"Data saved to '{filename}' successfully.")
        else:
            print("No data to save.")

    def main(self):
        headings_data = self.extract_headings()
        if headings_data:
            self.write_to_csv(headings_data, 'AllPagesDataOutput.csv')
        else:
            print("No headings data found.")


url = "https://packaging.python.org/en/latest/"

scraper = WebScraper(url)
scraper.main()
