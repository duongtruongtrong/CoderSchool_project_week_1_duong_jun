import requests

from bs4 import BeautifulSoup

def get_html(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    

number_of_product = 1

while number_of_product > 0:
    # Tiki - Tivi category
    r = requests.get('https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page=1')

    soup = r

    stop at page that does not contain any product