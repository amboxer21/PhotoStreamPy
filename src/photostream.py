#!/usr/bin/env python

import re
import sys
import time
import wget

from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class MetaPhotostream(type):

    def __new__(meta,name,bases,dct):
        return super(MetaPhotostream, meta).__new__(meta, name, bases, dct)

    def __init__(cls,name,bases,dct):
        if not hasattr(cls,'count'):
            cls.count = 0
        if not hasattr(cls,'driver'):
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
            profile    = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", user_agent)
            cls.driver = webdriver.Firefox(profile)

class Photostream(metaclass=MetaPhotostream):

    def __init__(self,config_dict={}):
        self.email        = config_dict['email']
        self.timeout      = config_dict['timeout']
        self.password     = config_dict['password']
        self.username     = config_dict['username']
        self.directory    = config_dict['directory']

        if not all([self.directory, self.username]):
            print('FB username and save directory must be specified!')
            Photostream.driver.close()
            sys.exit(0)

    def login(self):
        Photostream.driver.get("https://www.facebook.com/login")
        uname = Photostream.driver.find_element_by_name("email")
        uname.send_keys(self.email)
        pword = Photostream.driver.find_element_by_name("pass")
        pword.send_keys(self.password,Keys.RETURN)
        time.sleep(5)

    def scroll_to_bottom(self):
        try:
            while Photostream.count < self.timeout:
                Photostream.count += 1
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                try:
                    end = self.driver.find_element_by_xpath("//*[contains(text(), 'This bogus string will never be found')]")
                    if end.text is not None:
                        break
                except NoSuchElementException:
                    pass
        except Exception as exception:
            print('Exception exception: '+str(exception))
            pass

    def main(self):
        Photostream.driver.get("https://www.facebook.com/"+str(self.username)+"/photos_all")
        self.scroll_to_bottom()
        images = Photostream.driver.find_elements_by_xpath('//i[@style]')
        for image in images:
            url = image.get_attribute("style")
            results = re.search('(background-image: url\(")(.*)("\);)', str(url), re.M | re.I)
            if results is not None:
                try:
                    wget.download(results.group(2),out=self.directory)
                except:
                    pass

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-e', '--email',
        dest='email', default='example@email.com',
        help='This is your Facebook E-mail.')
    parser.add_option('-p', '--password',
        dest='password', default='password',
        help='This is your Facebook login password.')
    parser.add_option('-t', '--timeout',
        dest='timeout', type='int', default=120,
        help='How long the program will scroll to reach the bottom of your photo page.')
    parser.add_option('-O', '--directory',
        dest='directory',
        help='Where the photos will be saved.')
    parser.add_option('-u', '--username',
        dest='username',
        help='This is your Facebook user name.')
    (options, args) = parser.parse_args()

    config_dict = {
      'email'        : options.email,
      'timeout'      : options.timeout,
      'password'     : options.password,
      'username'     : options.username,
      'directory'    : options.directory,
    }

    photostream = Photostream(config_dict)
    photostream.login()
    photostream.main()
