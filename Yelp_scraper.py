from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import os,sys,re
import time
import csv
import json

'''
yelp_search_page class is used to get the features from the yelp search page
'''

class yelp_search_page():
    def __init__(self,driver): #####assign the driver to teh class first
        self.driver = driver
        self.search_page = 'https://www.yelp.com/'
    
    '''
    input: at least one of the catrgories: store_name or location
    '''   
    def search(self,store_name = '',location = ''):
        self.driver.get(self.search_page)
        time.sleep(1)
        if store_name == '' and location == '':
            print("Error, please input at least one of the categories: store_name or location")
        else:
            self._input_name(store_name)
            self._input_location(location)
            self._click_search_button()
            
    def _input_name(self,store_name):
        try:
            name_input = self.driver.find_element_by_css_selector("input[id ^= 'find_desc']")
            name_input.clear()
            name_input.send_keys(store_name)
        except:
            print("Can't input store name")
            
    def _input_location(self,location):
        try:
            loc_input = self.driver.find_element_by_css_selector("input[id ^= 'dropperText_Mast']")
            loc_input.clear()
            loc_input.send_keys(location)
        except:
            print("Can't input location")
            
    def _click_search_button(self):
        try:
            search_button = self.driver.find_element_by_css_selector("button[id ^= 'header-search-submit']")
            search_button.click()
        except:
            print("Can't click search button")
    
    
    def has_no_result(self):
        try:
            if "no result" in self.driver.find_element_by_css_selector("h1[class = 'css-ve950e']").text.lower():
                return True
            else:
                return False
        except:
            return False
        
    '''
    return: list of store with features (link,name,address,attribute)
    '''
    def get_store_list(self):
        store_list = [] ####### all store information under this search term
        while self._has_next_page:
            try:
                store_list += self._get_page_stores()
                self._move_to_next_page()
            except:
                break
        return store_list
    
    def _move_to_next_page(self):
        self.driver.find_element_by_css_selector("a[class ^= 'next-link']").click()
    
    def _has_next_page(self):
        try:
            self.driver.find_element_by_css_selector("a[class ^= 'next-link']")
            return True
        except:
            return False
    
    #######return the store information from one page
    def _get_page_stores(self):
        page_store_list = [] #######the store information in one page
        store_tokens =  self.driver.find_elements_by_css_selector("div[class ^= ' scrollablePhotos__09f24__1PpB8']")
        for token in store_tokens:
            store_info = {}
            store_info['link'] = self._get_store_link(token)
            store_info['name'] = self._get_store_name(token)
            store_info['address'] = self._get_store_address(token)
            store_info['attribute'] = self._get_store_attribute(token)
            page_store_list.append(store_info)
        return page_store_list
    
    def _get_store_link(self,token):
        try:
            return token.find_element_by_css_selector("a[class ^= 'css-166la90']").get_attribute('href')
        except:
            return False
    
    def _get_store_name(self,token):
        try:
            return token.find_element_by_css_selector("a[class ^= 'css-166la90']").text
        except:
            return False  
    
    def _get_store_address(self,token):
        try:
            return token.find_element_by_css_selector("address").text
        except:
            return False
    
    def _get_store_attribute(self,token):
        try:
            return token.find_element_by_css_selector("div[class ^= ' priceCategory__09f24__2IbAM']").text
        except:
            return False


# In[22]:


'''
yelp_store_page class is used to get the features from the yelp store page
'''

class yelp_store_page():
    def __init__(self,driver): #####assign the driver to teh class first
        self.driver = driver
        
    '''
    input: store link, assign the link to driver
    '''    
    def go_to(self,link):
        try:
            self.driver.get(link)
            return True
        except:
            print("Can't access link: " + str(link))
            return False
            
    def get_store_info(self,link):
        store_info = {}
        store_info['link'] = link
        store_info['name'] = self.get_name()
        store_info['rate'] = self.get_rate()
        store_info['num_reviewer'] = self.get_num_reviewer()
        store_info['price'] = self.get_price()
        store_info['attribute'] = self.get_attribute()
        store_info['is_claimed'] = self.is_claimed()
        store_info['coordinate'] = self.get_geo()
        store_info['address'] = self.get_address()
        return store_info
    
    def get_name(self):
        try:
            return self.driver.find_element_by_css_selector("h1[class ^= 'css-11q1g5y']").text
        except:
            return False
        
    def get_rate(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photoHeader__373c0__YdvQE']")
                return header.find_element_by_css_selector("div[class ^= ' i-stars__373c0__1BRrc']").get_attribute("aria-label")
            except:
                header = self.driver.find_elements_by_css_selector("div[class = ' arrange__373c0__2C9bH gutter-2__373c0__1DiLQ border-color--default__373c0__3-ifU']")[1]
                return header.find_element_by_css_selector("div[class ^= ' i-stars__373c0__1BRrc']").get_attribute("aria-label")
        except:
            return ''
        
    def get_num_reviewer(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photoHeader__373c0__YdvQE']")
                for tag in header.find_elements_by_css_selector("span[class ^= ' css-bq71j2']"):
                    if 'review' in tag.text.lower():
                        return tag.text

            except:
                header = self.driver.find_elements_by_css_selector("div[class = ' arrange__373c0__2C9bH gutter-2__373c0__1DiLQ border-color--default__373c0__3-ifU']")[1]
                for tag in header.find_elements_by_css_selector("span[class ^= ' css-1h1j0y3']"):
                    if 'review' in tag.text.lower():
                        return tag.text

        except:
            return ''
        return ''
    
    def get_price(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photoHeader__373c0__YdvQE']")
                for tag in header.find_elements_by_css_selector("span[class ^= ' css-1xxismk']"):
                    if '$' in tag.text.lower():
                        return tag.text

            except:
                header = self.driver.find_elements_by_css_selector("div[class = ' arrange__373c0__2C9bH gutter-2__373c0__1DiLQ border-color--default__373c0__3-ifU']")[1]
                for tag in header.find_elements_by_css_selector("span[class ^= ' css-1xxismk']"):
                    if '$' in tag.text.lower():
                        return tag.text

        except:
            return ''
        return ''
    
        
    def get_attribute(self):
        attribute = []
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photoHeader__373c0__YdvQE']")
                for tag in header.find_elements_by_css_selector("a[class ^= 'css-166la90']"):
                    if 'unclaimed' in tag.text.lower():
                        continue
                    attribute.append(tag.text)
            except:
                header = self.driver.find_elements_by_css_selector("div[class = ' arrange__373c0__2C9bH gutter-2__373c0__1DiLQ border-color--default__373c0__3-ifU']")[1]
                for tag in header.find_elements_by_css_selector("a[class ^= 'css-166la90']"):
                    if 'unclaimed' in tag.text.lower():
                        continue
                    attribute.append(tag.text)
        except:
            return attribute
        return attribute     
    
    def is_claimed(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photoHeader__373c0__YdvQE']")
                for tag in header.find_elements_by_css_selector("span[class ^= 'claim-text--light__373c0__1ip1u']"):
                    if tag.text.lower() == 'claimed':
                        return True
                return False
            except:
                header = self.driver.find_elements_by_css_selector("div[class = ' arrange__373c0__2C9bH gutter-2__373c0__1DiLQ border-color--default__373c0__3-ifU']")[1]
                for tag in header.find_elements_by_css_selector("span[class ^= 'claim-text--dark__373c0__xRoSM']"):
                    if tag.text.lower() == 'claimed':
                        return True
                return False
        except:
            return False
        
    def get_geo(self):
        coordinates = {}
        try:
            map_link_content = self.driver.find_element_by_css_selector("div[class ^= ' container__373c0__u8fHx'] > img").get_attribute("src").split('&')
            for content in map_link_content:
                if 'center' in content.lower():
                    content = content.replace("center=","")
                    content = content.split("%2C")
                    coordinates["latitude"] = content[0]
                    coordinates["longitude"] = content[1]
                    return coordinates
            return coordinates
        except:
            return coordinates
        
    def get_address(self):
        try:
            return self.driver.find_element_by_css_selector("address").text.replace('\n',',')
        except:
            return ''


