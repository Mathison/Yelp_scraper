###return the list of comment box
def get_comments_box_list(driver):
    try:
        comments_list = driver.find_elements_by_css_selector("div[class = ' review__09f24__oHr9V border-color--default__09f24__NPAKY']")
        return comments_list  ###the first comments is just the regular blank one for user
    except Exception as e:
        print(e)
        return False


def get_comment_info(comment_box):
    result_comment = {}
    name,user_url = get_name_and_url(comment_box)
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
    
###return the name and the user profile link from the comment box
def get_name_and_url(comment_box):
    try:
        name_box = comment_box.find_element_by_css_selector("a[class='css-1m051bw']")
        return name_box.text, name_box.get_attribute("href")
    except Exception as e:
        return False, False
        
###return the time from the comment box
def get_time(comment_box):
    try:
        time = comment_box.find_element_by_css_selector("span[class = ' css-chan6m']").text
        return time.split('\n')[0]
    except Exception as e:
        return False

###return rate
def get_rate(comment_box):
    try:
        rate = comment_box.find_element_by_css_selector("div[class ^= ' i-stars__09f24__M1AR7']").get_attribute("aria-label")
        return rate.split(' ')[0]
    except Exception as e:
        return False

###return text from comment box
def get_text(comment_box):
    try:
        text = comment_box.find_element_by_css_selector("span[class = ' raw__09f24__T4Ezm']").text
        return text
    except Exception as e:
        return False

##return location'
def get_location(comment_box):
    try:
        loc = comment_box.find_element_by_css_selector("span[class = ' css-qgunke").text
        return loc
    except Exception as e:
        print(e)
        return False

def get_attribute(comment_box):
    attribute_dict = {}
    ###########return the three attribute box Useful, Funny, Cool
    three_attributes = comment_box.find_elements_by_css_selector("span[class ^= ' display--inline__09f24__c6N_k']")
    for box in three_attributes:
        try:
            point = box.find_element_by_css_selector("span[class = ' css-1lr1m88']").text
        except:
            point = 0
        if 'Useful' in box.text:
            attribute_dict['Useful'] = point
            
        if 'Funny' in box.text:
            attribute_dict['Funny'] = point
            
        if 'Cool' in box.text:
            attribute_dict['Cool'] = point
            
    return attribute_dict
