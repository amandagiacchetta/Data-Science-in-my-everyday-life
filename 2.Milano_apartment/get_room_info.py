
from selenium import webdriver
import pandas as pd
import time
import dotenv
import os


dotenv.load_dotenv(dotenv.find_dotenv())
path = os.getenv('chrome_driver')

site = os.getenv('site')

driver = webdriver.Chrome(path)
driver.get(site)

#gets the data from the text of the tag
def get_info(tag, classe):
    info = driver.find_elements_by_xpath(f'//{tag}[@class="{classe}"]')
    info_list = [info[i].text for i in range(len(info))]
    return info_list

#gets the data from a attribute of the tag
def get_attribute(tag, classe, attribute):
    elements = driver.find_elements_by_xpath(f'//{tag}[@class="{classe}"]')
    return [elements[i].get_attribute(f"{attribute}") for i in range(len(elements))]
    
#gets the data from all tags and creates a dataframe
def get_data():

    room_ids = get_attribute('div', "searchResultWrapper", "data-bed-id")
    address = get_info("div", "searchResultAddress")
    price = get_info('div', "price")
    results = get_info('li', 'searchResult')
    images = get_attribute('img','solutionImage','src')
    
    dict = {"ids":room_ids, "results": results, "address": address, "price":price,"images":images}

    data = pd.DataFrame(dict)

    return data


def main():

    #get first batch of data
    data = get_data()

    #click on the button to prevent overlapping
    driver.find_element_by_xpath('//button[@class="cookieAgree"]').click()
    
    #find the number of the actual page
    actual_page = int(get_attribute('li', "paginationjs-page J-paginationjs-page active", "data-num").pop(0))
    
    #find the number from the last page
    final_page= int(get_attribute('li', "paginationjs-page paginationjs-last J-paginationjs-page", "data-num").pop(0))
    
    #create a varible to be able to move the cursor over pages 
    pagina = int(actual_page + 1)

    #loop over the pages until the final_page

    while pagina <= final_page:
        
        #click on the next page
        driver.find_element_by_xpath(f'//li[@data-num="{pagina}"]').click()
        time.sleep(1)

        #get the data 
        data_cont = get_data()

        #concat the data with the first batch
        data = pd.concat([data, data_cont], ignore_index=True)

        #update the page variable
        pagina = pagina + 1
    
    data.to_pickle('data/dovevivo.pkl')

        
if __name__ == "__main__":
    main() 


