from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .models import What_i_want


def amazon(item_url):
    uClient = uReq(item_url)
    page_html = uClient.read()
    uClient.close()
    page = soup(page_html, "lxml")

    item = page.findAll("div", {"class":"s-item-container"})

    item_list = []

    for i in item:
        if i.h2 is not None:
            title = i.h2.text
            #print (title)
            item_title = []
            item_title.append(title)
            db_title = What_i_want(item_title = title)
            rate = i.findAll("span", {"class":"a-icon-alt"})

            if rate == [] or len(rate) == 1:
                db_rating = What_i_want(item_rating = 'No rating available')
                item_title.append('No rating available')
                #print('No rating available')
            else:
                item_title.append(rate[1].text)
                db_rating = What_i_want(item_rating = rate[1].text)
                #print (rate[1].text)

            wholeprice = i.findAll("span", {"class":"a-offscreen"})
            factural = i.findAll("span", {"class":"a-size-base a-color-base"})

            if wholeprice != []:
                price = wholeprice[0].text
            elif wholeprice ==[] and factural == []:
                price = 'Not a valid product'
            else:
                price = factural[0].text
            db_price = What_i_want(item_price = price)
            item_title.append(price)
            #print(price)
            #print ('')
        db_rating.save()
        db_title.save()
        db_price.save()
        item_list.append(item_title)
    return item_list

def search_amazon(wanted_item):

    options = Options()
    """options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")"""

    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

    #driver = webdriver.Chrome(executable_path='/mnt/c/Users/TheOn/AppData/Local/Programs/Python/Python36-32/selenium/webdriver/chromedriver_win32/chromedriver.exe', chrome_options=options)
    driver = webdriver.Chrome(executable_path='/mnt/c/Users/TheOn/AppData/Local/Programs/Python/Python36-32/selenium/webdriver/chromedriver_win32/chromedriver.exe', chrome_options=options)
    #driver = webdriver.Chrome("/mnt/c/Users/TheOn/AppData/Local/Programs/Python/Python36-32/selenium/webdriver/chromedriver_win32/chromedriver.exe")
    driver.get('https://amazon.com')
    search_box = driver.find_element_by_id('twotabsearchtextbox')
    search_box.send_keys(wanted_item)
    search_box.submit()
    item_url = driver.current_url
    driver.quit()
    print(item_url)
    return item_url
