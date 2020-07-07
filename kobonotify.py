#! python3
# kobonotify.py
# 
# This checks to see if the 32GB version of the Kobo Forma is in stock
# on the Kobo website, and sends a text notification using the Twilio API.
#
# More specifically, it checks to see when it says something other than 
# "Out of Stock", to allow for pricing changes.
#
#
# The Twilio feature requires the creation of a separate file called,
# "kobonotifyconfig.py" which contains private info not to be included in
# a github repo, namely phone numbers and Twilio API keys. This config file
# should have the following four functions:
#
#  def twilio_sid():
#    return('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#
# def twilio_authtoken():
#    return('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#
# def twilio_num():
#    return('+12223334444')
#
# def my_num():
#    return('+12223334444')
#
# twilio_sid is your Twilio account SID
# twilio_authtoken is your Twilio auth token
# twilio_num is your Twilio phone number
# my_num is the phone number you want notification texts to go to
#
# It was only after I set this all up that I realized I could have just
# created something that imported as a list, and I need to research other
# ways to create config files, and other ways to keep API keys secure

import time, sys, datetime
from twilio.rest import Client
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import kobonotifyconfig as kcon

# Make the browser run headless
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

kobo_oos = True # Variable that is True when the Forma 32GB is not in stock,

# Get the Twilio keys and phone #s from the config file
sid = kcon.twilio_sid()
auth = kcon.twilio_authtoken()
twilio_num = kcon.twilio_num()
my_num = kcon.my_num()


# Send a test text via Twilio to confirm that is working

twilioCli = Client(sid, auth)
test_message = twilioCli.messages.create(body="Just confirming this thing actually works!", from_=twilio_num, to=my_num)

while kobo_oos == True:

    # Use a headless Firefox Webdriver to find the Add button and get its value

    browser = webdriver.Firefox(options=options)

    # URL of Kobo Forma as of May 22, 2020
    browser.get('https://ca.kobobooks.com/products/kobo-forma?variant=17773350617193')
    #browser.get('https://ca.kobobooks.com/products/kobo-forma?variant=13592985862249')

    # Close the popup
    try:
        close_popup = browser.find_element_by_id('fancybox-close')
        close_popup.click()
    except NoSuchElementException:
        continue
    try:
        forma_status = browser.find_element_by_name('add').get_attribute('value')
        now = datetime.datetime.now()
        # Print timestamp of the last check results, mainly to let me know that it's still running
        print('Status as of ' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute).zfill(2) + ' --> ' + forma_status)
        if forma_status != "Out of Stock":
            break

    except NoSuchElementException:
        print("Can't find the 'add' button\n\nSomething important about the page has changed")
        sys.exit()
    
    # Close the browser process
    browser.close()

    

    # Check every 20 minutes
    time.sleep(1200)

# If the loop is broken, then the 32GB Forma is back in stock. Send a text message alerting!
test_message = twilioCli.messages.create(body="Looks like the 32GB Kobo Forma is back in stock, bud!", from_=twilio_num, to=my_num)