import requests

from bs4 import BeautifulSoup

data_col = ['data-seller-product-id',
'product-sku',
'data-title',
'data-price',
'data-id',
'data-brand',
'data-category',
'product_link',
'product_image',
'price-regular',
'sale-tag sale-tag-square',
'rating_percentage',
'number_of_reviews']

output_dict = {}
for col in data_col:
    output_dict[col] = []

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

    get_data(item_html)
    item_html: HTML of each item in item_list, type: string
    """

    # dictionary with keys and values are list
    d = output_dict
    # get general_info
    for i in data_col_dict['general_info']:
        d[i].append(item_html[i])
    
    # get links
    d['product_link'].append(item_html.a['href'])
    d['product_image'].append(item_html.a.img['src'])

    # get price
    for i in data_col_dict['price']:
        d[i].append(item_html.find('span', {'class':i}).text)
    
    # get rating_percentage
    rating_section = item_html.find('div', {'class':'review-wrap'})

    d['number_of_reviews'].append(rating_section.find('p', {'class':'review'}).text)

    # getting to rating_percentage
    p_rating = rating_section.find('p', {'class':'rating'})
    span_rating = p_rating.find('span', {'class':'rating-content'})

    d['rating_percentage'].append(span_rating.span['style'])

    return d


    

tiki_link = 'https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page=1'

# get_item_list(get_html(tiki_link))[0]
for item_html in get_item_list(get_html(tiki_link))[:2]:
    output_dict = get_data(item_html, output_dict)

print(output_dict)

# help(get_html)
# help(get_item_list)

# number_of_product = 1

# while number_of_product > 0:
#     # Tiki - Tivi category
#     r = requests.get('https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page=1')

#     soup = r

#     stop at page that does not contain any product