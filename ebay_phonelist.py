from bs4 import BeautifulSoup
from bs4.element import AttributeValueWithCharsetSubstitution
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import pandas as pd 
from datetime import date
import time

ubicacion = r'C:/Users/Josve/AppData/Local/Programs/Python/Python39/Lib/site-packages/selenium/webdriver/chromedriver.exe'
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path= ubicacion)

home_link = "https://www.ebay.com/"
search_kw = "iPhone 12".replace(" ","+")

driver.get(home_link+"sch/i.html?_from=R40&_trksid=p2334524.m570.l2632&_nkw=iphone+12&_sacat=9355&LH_TitleDesc=0&_odkw="+search_kw+"&_osacat=0")

phone_title = []
phone_link = []
phone_status = []
phone_score = []
phone_reviews_amt = []
phone_price = []
phone_location = []

pg_mount = 5
page = BeautifulSoup(driver.page_source, 'html.parser')

for i in range(0,pg_mount):
  for phone in page.findAll('li', attrs={'class':'s-item','data-view':True}):
    title = phone.find('h3', attrs={'class': 's-item__title'})
    if title: 
      phone_title.append(title.text)
    else: phone_title.append('')

    link = phone.find('a', attrs={'class': 's-item__link'})
    if link:
      phone_link.append(link['href'])
    else: phone_link.append('')

    status = phone.find('div', attr={'class': 's-item__subtitle'})
    if status:
      phone_status.append(status.text)
    else: phone_status.append('')

    score = phone.find('div', attrs={'class':['b-starrating','x-star-rating']})
    if score:
      score.find('span', attrs={'class':'clipped'})
      if score:
        phone_score.append(score.text[0:3])
      else: phone_score.append('')
    else: phone_score.append('')

    reviews_amt = phone.find('span', attrs={'class':'s-item__reviews-count'})
    if reviews_amt:
      phone_reviews_amt.append(reviews_amt.span.text[0:reviews_amt.span.text.find('valor')-1])
    else: phone_reviews_amt.append('')

    price = phone.find('span', attrs={'class':'s-item__price'})
    if price:
      phone_price.append(float(''.join((price.text[4:(price.text+ ' a').find(' a')]).split())))

    location = phone.find('span', attrs={'class':'s-item__location'})
    if location:
      phone_location.append(location.text[3:])
    else: phone_location.append('')

next_btn = driver.find_element_by_css_selector('.pagination__next')
next_btn.click()
time.sleep(2) 

phone_list = pd.DataFrame({
                            'TITLE':phone_title,
                            'STATUS':phone_status,
                            'SCORE':phone_score,
                            'REVIEWS_AMT':phone_reviews_amt,
                            'PRICE':phone_price,
                            'LOCATION':phone_location,
                            'LINK':phone_link
                        })

phone_list = phone_list.sort_values(by=['PRICE','SCORE','REVIEWS_AMT'], ascending=[True,False,False])

phone_list.to_excel('phone_list.xlsx', index=None, header=True, encoding='utf-8-sig')