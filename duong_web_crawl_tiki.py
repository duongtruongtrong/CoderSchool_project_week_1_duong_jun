import requests

from bs4 import BeautifulSoup

import pandas as pd

import time

import random

data_col = {'data-seller-product-id':'product_id',
'product-sku':'product_sku',
'data-title':'product_name',
'data-price':'current_price',
'data-id':'data_id',
'data-brand':'product_brand',
'data-category':"category",
'product_link':'product_link',
'product_image':'product_image_link',
'price-regular':'original_price',
'sale-tag sale-tag-square':'discount_pct',
'rating_percentage':'rating_pct',
'number_of_reviews':'number_of_reviews'}

data_col_dict = {'general_info': ['data-seller-product-id',
'product-sku',
'data-title',
'data-price',
'data-id',
'data-brand',
'data-category'],

'product_link': 'product_link',

'product_image': 'product_image',

'price':['price-regular',
'sale-tag sale-tag-square'],

'rating_percentage':'rating_percentage',
'number_of_reviews':'number_of_reviews'
}

def get_html(link):
    """From URL return HTML code in the website.

    get_html(link)
    link: URL of the website, type: string
    """

    # get website data
    r = requests.get(link)

    # turn website data text to HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup

def get_item_list(full_webpage_html):
    """From HTML string return HTML string containing item list section on Tiki website.
    Then, get all items in the section as a list
    Only tested on Tiki TV category webpage.

    get_item_list(full_webpage_html)
    full_webpage_html: HTML of a full Tiki website page, type: string
    """
    
    # crawl class='product-box-list' section
    item_section = full_webpage_html.find('div', {'class':'product-box-list'})

    item_list = item_section.find_all('div', {"class":"product-item"})

    return item_list

def get_data(item_html, output_dict):
    """Get data from item_list HTML for selected data_col list.
    Return a dictionary.

    If can't crawl the data, give None value.
    Reasons for can not crawl data:
        - No such tag/attribut: No review

    get_data(item_html)
    item_html: HTML of each item in item_list, type: string
    """

    # dictionary with keys and values are list
    d = output_dict

    # if can't crawl the data, give None value.
    # Reason for can not crawl data:
    #     - No such tag/attribut: No review

    # get general_info
    for i in data_col_dict['general_info']:
        try:
            d[i].append(item_html[i])
        except:
            d[i].append(None)
    
    # get links
    try:
        d['product_link'].append(item_html.a['href'])
    except:
        d['product_link'].append(None)

    try:
        d['product_image'].append(item_html.a.img['src'])
    except:
        d['product_image'].append(None)

    # get price
    for i in data_col_dict['price']:
        try:
            d[i].append(item_html.find('span', {'class':i}).text)
        except:
            d[i].append('0')
    
    # get rating_percentage
    try:
        rating_section = item_html.find('div', {'class':'review-wrap'})
    
        d['number_of_reviews'].append(rating_section.find('p', {'class':'review'}).text)
    except:
        d['number_of_reviews'].append('0')

    # getting to rating_percentage
    try:
        p_rating = rating_section.find('p', {'class':'rating'})
        span_rating = p_rating.find('span', {'class':'rating-content'})
        
        d['rating_percentage'].append(span_rating.span['style'])
    except:
        d['rating_percentage'].append('0')

    return d

try:
    df_output = pd.read_excel('tiki_tv_product.xlsx')
except:
    df_output = pd.DataFrame()

number_of_product = 1

# start with 1 | start with the previous page + 1
if len(df_output) == 0:
    page_number = 1
else:
    # start the next page from the last page in df_output
    page_number = df_output['page'].max() + 1

# tiki link without page number
tiki_link = 'https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page='

while number_of_product > 0:
    
    # get HTML from tiki_link + page_number
    # f'https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page={page_number}'
    full_html = get_html(tiki_link + str(page_number))

    # get item list from full_html
    item_list = get_item_list(full_html)
    number_of_product = len(item_list)

    # if there is not produc in item list, it means it reach the last page.
    if number_of_product > 0:

        # initiate output_dict to store the page result
        output_dict = {}
        for col in data_col:
            output_dict[col] = []

        # get all the data
        for item_html in item_list:
            output_dict = get_data(item_html, output_dict)
        
        # output df
        df = pd.DataFrame(data = output_dict, columns = output_dict.keys())
        df['page'] = page_number

        # cleaning df
        df['price-regular'] = df['price-regular'].str.replace(r'\.|đ', '').astype(int)
        
        df['product_link'] = 'https://tiki.vn/'+ df['product_link']

        df['rating_percentage'] = df['rating_percentage'].str.replace(r'width:|%', '').astype(float)

        df['number_of_reviews'] = df['number_of_reviews'].str.replace(r'\(| nhận xét\)', '').astype(int)

        df['sale-tag sale-tag-square'] = df['sale-tag sale-tag-square'].str.replace(r'-|%', '').astype(float)

        df.rename(columns=data_col, inplace=True)

        # merge/concat with the last df output df_output
        if len(df_output) != 0:
            df_output = pd.concat([df_output, df], sort=False)
        else:
            df_output = df

        # save to excel file after every page finish crawling
        df_output.to_excel('tiki_tv_product.xlsx', index=False)

        finish_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f'Finish crawling page {page_number} at {finish_time}')

    page_number+=1

    time.sleep(random.randint(2, 4))

print('Finish crawling!')

print(df_output.info())