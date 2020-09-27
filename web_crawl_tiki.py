import requests
r = requests.get('https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner')
# print(r.text)
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify()[:500])
body_soup = soup.body
# print(body_soup.prettify())
section_1_soup = body_soup.find('div', {'data-seller-product-id':'17465704'}) 
print(section_1_soup['data-seller-product-id'])
print(section_1_soup['data-brand'])
print(section_1_soup['data-category'])
print(section_1_soup['data-id'])
print(section_1_soup['data-price'])
print(section_1_soup['data-score'])
print(section_1_soup['data-title'])
print(section_1_soup['product-sku'])
Product_link = section_1_soup.find('a')
Product_link['href']

Product_image = section_1_soup.find('img')
Product_image['src']

section_2_soup = section_1_soup.find('span', {'class':'price-regular'})
print(section_2_soup.text)

section_3_soup = section_1_soup.find ('span', {'class':'sale-tag sale-tag-square'})
print(section_3_soup.text)

gucci_2_soup = body_soup.find('p', {'class':'rating'}) 
gucci_3_soup = gucci_2_soup.find('span', {'style':'width:92%'})
gucci_4_soup = body_soup.find('div', {'class':'review-wrap'})
gucci_5_soup = gucci_4_soup.find ('p', {'class':'review'})

print(gucci_3_soup['style'])
print(gucci_5_soup.text)
