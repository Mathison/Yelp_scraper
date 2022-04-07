from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from yelp_comment_scrape import get_comments_box_list,get_comment_info

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
            try:
                name_input = self.driver.find_element_by_css_selector("input[id = 'search_description']")
            except:
                name_input = self.driver.find_element_by_css_selector("input[id = 'find_desc']")
            name_input.clear()
            name_input.send_keys(store_name)
        except:
            print("Can't input store name")
            
    def _input_location(self,location):
        try:
            try:
                loc_input = self.driver.find_element_by_css_selector("input[id = 'search_location']")
            except:
                loc_input = self.driver.find_element_by_css_selector("input[id = 'dropperText_Mast']")
            loc_input.clear()
            loc_input.send_keys(location)
        except:
            print("Can't input location")
            
    def _click_search_button(self):
        try:
            try:
                search_button = self.driver.find_element_by_css_selector("button[data-testid = 'suggest-submit']")
            except:
                search_button = self.driver.find_element_by_css_selector("button[id = 'header-search-submit']")
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
                time.sleep(3)
            except:
                break
                
        duplicate_link = []
        unique_store = []
        for data in store_list:
            link = data['link'].split('?')[0]
            if link in duplicate_link:
                continue
            duplicate_link.append(link)
            unique_store.append(data)
        return unique_store
    
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
        store_tokens =  self.driver.find_elements_by_css_selector("div[class ^= ' container__09f24__mpR8_']")
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
            return token.find_element_by_css_selector("a[class ^= 'css-1m051bw']").get_attribute('href')
        except:
            return False
    
    def _get_store_name(self,token):
        try:
            return token.find_element_by_css_selector("a[class ^= 'css-1m051bw']").text
        except:
            return False  
    
    def _get_store_address(self,token):
        try:
            return token.find_element_by_css_selector("span[class = ' css-chan6m']").text
        except:
            return False
    
    def _get_store_attribute(self,token):
        try:
            return token.find_element_by_css_selector("p[class ^= 'css-dzq7l1']").text
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
    
            
    def get_store_info(self,link):
        store_info = {}
        if not self.go_to(link):
            return store_info
        time.sleep(1)
          
        store_info['link'] = self.driver.current_url
        store_info['name'] = self.get_name()
        store_info['rate'] = self.get_rate()
        store_info['num_reviewer'] = self.get_num_reviewer()
        store_info['price'] = self.get_price()
        store_info['attribute'] = self.get_attribute()
        store_info['is_claimed'] = self.is_claimed()
        store_info['coordinate'] = self.get_geo()
        store_info['address'] = self.get_address()
        return store_info
    
    def go_to(self,link):
        try:
            self.driver.get(link)
            return True
        except:
            print("Can't access link: " + str(link))
            return False
        
    def get_name(self):
        try:
            return self.driver.find_element_by_css_selector("h1[class ^= 'css-12dgwvn']").text
        except:
            return False
        
    def get_rate(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photo-header-content__09f24__q7rNO']")
                return header.find_element_by_css_selector("div[class ^= ' i-stars__09f24__M1AR7']").get_attribute("aria-label")
            except:
                return self.driver.find_element_by_css_selector("div[class ^= ' i-stars__09f24__M1AR7']").get_attribute("aria-label")
        except Exception as e:
            print("rate",e)
            return ''
        
    def get_num_reviewer(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photo-header-content__09f24__q7rNO']")
                for tag in header.find_elements_by_css_selector("span[class ^= ' css-1fdy0l5']"):
                    if 'review' in tag.text.lower():
                        return tag.text

            except:
                tag = self.driver.find_element_by_css_selector("span[class ^= ' css-1p9ibgf']")
                if 'review' in tag.text.lower():
                    return tag.text

        except Exception as e:
            print("num reviewer",e)
            return ''
        return ''
    
    def get_price(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photo-header-content__09f24__q7rNO']")
                for tag in header.find_elements_by_css_selector("span[class ^= ' css-1ir4e44']"):
                    if '$' in tag.text.lower():
                        return tag.text

            except:
                return self.driver.find_element_by_css_selector("span[class ^= ' css-1ir4e44']").text.lower()
        except Exception as e:
            print("price",e)
            return ''
        return ''
    
        
    def get_attribute(self):
        attribute = []
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photo-header-content__09f24__q7rNO']")
                for tag in header.find_elements_by_css_selector("a[class ^= 'css-1m051bw']"):
                    if 'unclaimed' in tag.text.lower():
                        continue
                    attribute.append(tag.text)
            except:
                header = self.driver.find_elements_by_css_selector("span[class ^= ' css-1p9ibgf'] > a[class ^='css-1m051bw']")
                for tag in header:
                    if 'unclaimed' in tag.text.lower():
                        continue
                    attribute.append(tag.text)
        except Exception as e:
            print("attribute",e)
            return attribute
        return attribute     
    
    def is_claimed(self):
        try:
            try:
                header = self.driver.find_element_by_css_selector("div[class ^= ' photo-header-content__09f24__q7rNO']")
                for tag in header.find_elements_by_css_selector("span[class ^= 'claim-text--light__09f24__BSQOJ']"):
                    if tag.text.lower() == 'claimed':
                        return True
                return False
            except:
                
                for tag in self.driver.find_elements_by_css_selector("span[class ^= 'claim-text--dark__09f24__Hpw9d']"):
                    if tag.text.lower() == 'claimed':
                        return True
                return False
        except Exception as e:
            print("claimed",e)
            return False
        
    def get_geo(self):
        coordinates = {}
        try:
            map_link_content = self.driver.find_element_by_css_selector("div[class ^= ' container__09f24__fZQnf'] > img").get_attribute("src").split('&')
            for content in map_link_content:
                if 'markers=' in content.lower():
                    content = content.replace("2C","")
                    content = content.replace("7C","")
                    content = content.split('%')
                    coordinates["latitude"] = content[-1]
                    coordinates["longitude"] = content[-2]
                    return coordinates
            return coordinates
        except Exception as e:
            print("geo",e)
            return coordinates
        
    def get_address(self):
        try:
            return self.driver.find_element_by_css_selector("address").text.replace('\n',',')
        except:
            return ''


    def get_comments_list(self):
        comments_list = []
        while True:
            comments_box_list = get_comments_box_list(self.driver)
            if comments_box_list == False:
                break

            for comments_box in comments_box_list:
                result_comment = get_comment_info(comments_box)
                comments_list.append(result_comment)
            
            move = self.move_to_next_page()
            time.sleep(1)
            if move == False:
                break
        return comments_list
                
    ###return the next page url from that page
    ###return False if we reach the end
    def move_to_next_page(self):
        try:
            next_page = self.driver.find_element_by_css_selector("a[class ^= 'next-link']")
            next_page.click()
            return True
        except Exception as e:
            print(e)
            print("Reach final page")
            return False