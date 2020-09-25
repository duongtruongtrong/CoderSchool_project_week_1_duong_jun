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

def get_data(item_html):
    """Get data from item_list HTML for selected data_col list.

    get_data(item_html)
    item_html: HTML of each item in item_list, type: string
    """

    pass

tiki_link = 'https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page=1'



# help(get_html)
# help(get_item_list)

# number_of_product = 1

# while number_of_product > 0:
#     # Tiki - Tivi category
#     r = requests.get('https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page=1')

#     soup = r

#     stop at page that does not contain any product