# Welcome to the project_week_1_duong_jun!

# Crawling data of all Tiki product in TV category

## Overall Logic:
* **Step 1:** Crawl data of 1 item in page 1.
* **Step 2:** Loop step 1 to get all items in page 1.
* **Step 3:** Loop step 2 for all pages in Tiki category until the final page.

## Extra Features:
1. Extend an excel (.xlsx) file with crawled data of every page.
2. Continue the page where the script left off.

## Files:
1. data_columns.xlsx: Data need to crawl from Tiki webpage.
2. web_crawl_tiki.py: Get data of 1 item in page 1 (Step 1).
3. duong_web_crawl_tiki.py: Test loops with step 1 and step 2.
4. week_1_duong_jun_craw_tiki_category.py: Complete script with final result as .xlsx file.
5. tiki_tv_product.xlsx, tiki_tv_product.csv: Final result files.

## Python Code and Tips:
### Step 1: Crawl data of 1 item in page 1:
Author: Jun

Experiment with 1 item first in web_crawl_tiki.py

Use BeautifulSoup to crawl data on https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page

**Tip:** Use the bottom bar to get the exact level the HTML tag is on.
![image](https://user-images.githubusercontent.com/71629218/94356917-1d485d00-00be-11eb-9735-ec4ac0f11d6c.png)

### Step 2: Loop step 1 to get all items in page 1:
Author: Duong

Created 3 functions:
* get_html(link)
* get_item_list(full_webpage_html)
* get_data(item_html, output_dict): Use the result of Step 1

Use `for loop` with the above 3 functions:
* Get HTML from link 
  * -> Get the list of items in 1 page 
    * -> Loop through the list to get data of each item 
      * -> Extend to pre-generated dictionary.

Output dictionary format:
```
{'data-seller-product-id':[],
'product-sku':[],
'data-title':[],
...
'rating_percentage':[],
'number_of_reviews':[]}
```

**Tip:** Use `try except` if can't crawl the data to return None or '0' value for each element so that error won't stop the script.

### Step 3: Loop step 2 for all pages in Tiki category until the final page:
Author: Duong

Use `while loop` and stop when there is 0 product in the page ~ `len(list of items in 1 page) == 0`

1 page 1 loop.

**Tip:** Create a column in output file to store page number `df['page'] = page_number`.

### Extra Features:
Author: Duong

**Why need extra features:** Script can be interrupted at anytime, specially when crawling hundreds of pages.
* Don't want to lose the data the script crawled.
* Don't want to start over again.

### 1. Extend an excel (.xlsx) file with crawled data of every page:
Create a dataframe after each loop in the `while loop` -> Concat that dataframe to a master dataframe -> Export the master dataframe to a excel file.

### 2. Continue the page where the script left off:
Try to read output file (use `try except`) -> Get the **max page number** in the file -> The script starts from **max page number** + 1
