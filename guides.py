import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://packaging.python.org/en/latest/"

def fetch_page_content(url):
    """Fetches the page content and returns BeautifulSoup object"""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch page content from {url}")
        return None

def extract_headings(soup):
    """Extracts the main heading and subheadings from the page"""
    h1_text = soup.find('h1').get_text(strip=True) if soup.find('h1') else ""
    h2_texts = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
    return h1_text, h2_texts

def extract_pre_content(soup):
    """Extracts content inside the <pre> tag"""
    pre_text = soup.find('pre').get_text(strip=True) if soup.find('pre') else ""
    return pre_text

def process_link(link):
    """Processes the given link and extracts headings and content inside <pre> tag"""
    if link.startswith('..') or not link.startswith('http'):
        link = base_url + link.lstrip('../')
    soup = fetch_page_content(link)
    if soup:
        return extract_headings(soup), extract_pre_content(soup), link
    else:
        return (None, None, None), None

def process_category(category_tag, csv_writer):
    """Processes a category and its nested subcategories"""
    category_name = category_tag.find('a').get_text(strip=True)
    category_link = process_link(category_tag.find('a')['href'])[2]

    if category_link:
        # Extract headings and content inside <pre> tag from the category page
        (h1_text, h2_texts), pre_text, _ = process_link(category_link)
        # Write to CSV
        for h2_text in h2_texts:
            csv_writer.writerow([h1_text, h2_text, pre_text])

        # Process nested subcategories
        for subcategory_tag in category_tag.find_all('li', class_='toctree-l3'):
            subcategory_name = subcategory_tag.find('a').get_text(strip=True)
            subcategory_link = process_link(subcategory_tag.find('a')['href'])[2]

            if subcategory_link:
                # Extract headings and content inside <pre> tag from the subcategory page
                (_, sub_h2_texts), sub_pre_text, _ = process_link(subcategory_link)
                # Write to CSV
                for sub_h2_text in sub_h2_texts:
                    csv_writer.writerow([h1_text, sub_h2_text, sub_pre_text])

def main():
    with open("GuidesNestedPagesData.csv", "w", newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Heading", "Subheading", "Pre Content"])

        url = "https://packaging.python.org/en/latest/"
        soup = fetch_page_content(url)
        if soup:
            for category_tag in soup.find_all('li', class_='toctree-l2'):
                process_category(category_tag, csv_writer)

if __name__ == "__main__":
    main()
