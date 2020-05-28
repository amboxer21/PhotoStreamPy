#!/usr/bin/env python

import re
import sys
import time
import wget

from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class MetaPhotostreamSelenium(type):

    def __new__(meta,name,bases,dct):
        return super(MetaPhotostreamSelenium, meta).__new__(meta, name, bases, dct)

    def __init__(cls,name,bases,dct):
        if not hasattr(cls,'count'):
            cls.count = 0
        if not hasattr(cls,'member_list'):
            cls.member_list = {}
        if not hasattr(cls,'site_name'):
            cls.site_name = None
        if not hasattr(cls,'driver'):
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
            profile    = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", user_agent)
            cls.driver = webdriver.Firefox(profile)

class PhotostreamSelenium(metaclass=MetaPhotostreamSelenium):

    def __init__(self,config_dict={}):
        self.email        = config_dict['email']
        self.timeout      = config_dict['timeout']
        self.message      = config_dict['message']
        self.dry_run      = config_dict['dry_run']
        self.password     = config_dict['password']
        self.group_name   = config_dict['group_name']
        self.send_message = config_dict['send_message']

    def login(self):
        PhotostreamSelenium.driver.get("https://www.facebook.com/login")
        uname = PhotostreamSelenium.driver.find_element_by_name("email")
        uname.send_keys(self.email)
        pword = PhotostreamSelenium.driver.find_element_by_name("pass")
        pword.send_keys(self.password,Keys.RETURN)
        time.sleep(5)

    def scroll_to_bottom(self):
        try:
            iterator = 0
            while iterator < self.timeout:
                iterator += 1
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                try:
                    end = self.driver.find_element_by_xpath("//*[contains(text(), 'dgdfahdfhD')]")
                    if end.text is not None:
                        break
                except NoSuchElementException:
                    pass
        except Exception as exception:
            print('Exception exception: '+str(exception))
            pass

    def main(self,count=0):
        PhotostreamSelenium.driver.get("https://www.facebook.com/codecaine21/photos_all")
        self.scroll_to_bottom()
        images = PhotostreamSelenium.driver.find_elements_by_xpath('//i[@style]')
        for image in images:
            count += 1
            url = image.get_attribute("style")
            results = re.search('(background-image: url\(")(.*)("\);)', str(url), re.M | re.I)
            if results is not None:
                try:
                    wget.download(results.group(2),out='/home/anthony/Documents/Python/PhotoStream/Photos/')
                    #with open('/home/anthony/Documents/Python/PhotoStream/urls.txt','a') as f:
                        #f.write(str(results.group(2))+"\n")
                except:
                    pass

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-e', '--email',
        dest='email', default='example@email.com',
        help='This is your MeetUp E-mail.')
    parser.add_option('-p', '--password',
        dest='password', default='password',
        help='This is your MeetUp login password.')
    parser.add_option('-t', '--timeout',
        dest='timeout', type='int', default=120,
        help='Blah')
    (options, args) = parser.parse_args()

    config_dict = {
      'email'        : options.email,
      'timeout'      : options.timeout,
      'password'     : options.password,
    }

    meetupInactivityKicker = PhotostreamSelenium(config_dict)
    meetupInactivityKicker.login()
    meetupInactivityKicker.main()
