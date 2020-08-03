#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os,sys
import json
import time
import csv
import json


# In[2]:


def init_drive(drive_path):
    opts = Options()
    opts.add_argument("Chrome/78.0.3904.97")
    #opts.add_argument("Chrome/76.0.3809.100")
    #opts.add_argument("Chrome/71.0.3578.98")
    #opts.add_argument('--headless')

    opts.add_argument("--lang=en")
    drive = webdriver.Chrome(drive_path, chrome_options=opts)
    return drive


# In[18]:


def read_csv(path):
    data = []
    try:
        with open(path,'r',encoding = 'utf-16') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                data.append(row)
    except:
        with open(path,'r',encoding = 'utf-8') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                data.append(row)
    return data


# In[4]:


def write_csv(csv_list,path):
    with open(path, 'w',encoding='utf-16', newline = '') as csv_file:
        writer = csv.writer(csv_file)
        for item in csv_list:
            writer.writerow(item)


# In[72]:


###return the next page url from that page
###return False if we reach the end
def move_to_next_page(driver):
    try:
        next_page = driver.find_element_by_css_selector("a[class='lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']")
        next_page.click()
        return True
    except Exception as e:
        print(e)
        print("Reach final page")
        return False

    
    
###return the list of comment box
def get_comments_box_list(driver):
    try:
        comments_list = driver.find_elements_by_css_selector("div[class='lemon--div__373c0__1mboc review__373c0__13kpL sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__2C9bH gutter-2__373c0__1DiLQ grid__373c0__1Pz7f layout-stack-small__373c0__27wVp border-color--default__373c0__3-ifU']")
        return comments_list  ###the first comments is just the regular blank one for user
    except Exception as e:
        print(e)
        return False

###return the name and the user profile link from the comment box
def get_name(comment_box):
    try:
        name_box = comment_box.find_element_by_css_selector("a[class='lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']")
        return name_box.text, name_box.get_attribute("href")
    except Exception as e:
        return False, False
        
###return the time from the comment box
def get_time(comment_box):
    try:
        time = comment_box.find_element_by_css_selector("span[class = 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-']").text
        return time.split('\n')[0]
    except Exception as e:
        return False

###return rate
def get_rate(comment_box):
    try:
        rate = comment_box.find_element_by_css_selector("div[class ^= 'lemon--div__373c0__1mboc i-stars__373c0__1T6rz']").get_attribute("aria-label")
        return rate.split(' ')[0]
    except Exception as e:
        return False

###return text from comment box
def get_text(comment_box):
    try:
        text = comment_box.find_element_by_css_selector("span[class = 'lemon--span__373c0__3997G raw__373c0__3rKqk']").text
        return text
    except Exception as e:
        return False

##return location'
def get_location(comment_box):
    try:
        loc = comment_box.find_element_by_css_selector("span[class = 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO']").text
        return loc
    except Exception as e:
        print(e)
        return False


# In[56]:


def get_attribute(comment_box):
    attribute_dict = {}
    ###########return the three attribute box Useful, Funny, Cool
    three_attributes = comment_box.find_elements_by_css_selector("span[class = 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa- text-size--small__373c0__3NVWO']")
    for box in three_attributes:
        try:
            point = box.find_element_by_css_selector("span[class = 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--inherit__373c0__1lczC text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO']").text
        except:
            point = 0
        if 'Useful' in box.text:
            attribute_dict['Useful'] = point
            
        if 'Funny' in box.text:
            attribute_dict['Funny'] = point
            
        if 'Cool' in box.text:
            attribute_dict['Cool'] = point
            
    return attribute_dict


# In[69]:


def get_comment_info(comment_box):
    result_comment = {}
    name,user_url = get_name(comment_box)
    if name == False:
        name = ' '
    name = name.replace(',',' ')
    
    text = get_text(comment_box)
    if text == False:
        text = ' '
    text = text.replace(',',' ')
    text = text.replace('\n',' ')
    text = text.replace('\t',' ')
    
    location = get_location(comment_box)
    rate = get_rate(comment_box)
    time = get_time(comment_box)
    three_atrributes = get_attribute(comment_box)
    funny = three_atrributes['Funny']
    useful = three_atrributes['Useful']
    cool = three_atrributes['Cool'] 
    
    for att in [name,location,user_url,text,rate,time,funny,useful,cool]:
        if att == False:
            att = ' '
    result_comment['user_name'] = name
    result_comment['user_url'] = user_url
    result_comment['user_location'] = location
    result_comment['text'] = text
    result_comment['rate'] = rate
    result_comment['time'] = time
    result_comment['funny'] = funny
    result_comment['useful'] = useful
    result_comment['cool'] = cool
    return result_comment

#####return list of comments information
def search_one_store(driver,data):
    url = data[12]
    print(url)
    driver.get(url)
    time.sleep(1)
    
    result_json = {}
    result_json['index'] = data[0]
    result_json['name'] = data[2]
    result_json['type'] = data[10]
    result_json['link'] = data[12]
    result_json['comments'] = []
    
    while True:
        comments_list = get_comments_box_list(driver)
        if comments_list == False:
            break

        for comments_box in comments_list:
            result_comment = get_comment_info(comments_box)
            print(result_comment)
            result_json['comments'].append(result_comment)
            
        move = move_to_next_page(driver)
        time.sleep(1)
        if move == False:
            break
    return result_json


