import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup

products_details = []
base_url = 'https://www.jumia.com.dz/telephone-tablette/?page= #catalog-listing'
page_num = 1
max_pages =150


while page_num <= max_pages:
    url = base_url + str(page_num)
    print(f"Scraping page {page_num}: {url}")
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')


        if page_num == 1:
            limit_element = soup.find('p', {'class': '-gy5'})
            if limit_element:
                limit_text = limit_element.text
                try:
                    total_products = int(limit_text[:-15])
                    max_pages = int(np.ceil(total_products / 40))
                    print(f"Total Products: {total_products}, Max Pages: {max_pages}")
                except ValueError:
                    print("Error parsing total product count. Assuming 1 page.")
            else:
                print("Could not find total product count. Assuming 1 page.")

        products_list = soup.find_all('article', {'class': 'prd'})

        if not products_list:
            print("No products found on this page. Stopping.")
            break

        for product in products_list:
            try:
                products_name = product.find('h3', {'class': 'name'}).text.strip()
            except AttributeError:
                products_name = 'no name'
            try:
                products_price = product.find('div', {'class': 'prc'}).text.strip()
            except AttributeError:
                products_price = 'no price'
            try:
                products_rate = product.find('div', {'class': 'stars'}).text.strip()
            except AttributeError:
                products_rate = 'no stars'
            try:
                products_discount = product.find('div', {'class': 'dbg'}).text.strip()
            except AttributeError:
                products_discount = 'no discount'

            try:
                products_link_element = product.find('a', {'class': 'core'})
                if products_link_element:
                    products_link = "https://www.jumia.com.dz" + products_link_element.get('href')
                else:
                    products_link = "no link"
            except AttributeError:
                products_link = "no link"

            products_details.append({
                'website': 'jumia',
                'product price': products_price,
                'discount': products_discount,
                'product name': products_name,
                'product rate': products_rate,
                'product link': products_link,
            })

        time.sleep(2)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        break

    except Exception as e:
        print(f'Oops, something went wrong: {e}')
        break

    page_num += 1

jumia_df = pd.DataFrame.from_dict(products_details)
jumia_df.to_csv("jumia_data_tp.csv", header=True, index=False, encoding='utf-8')
print("Scraping complete. Data saved to jumia_data_tp.csv")



