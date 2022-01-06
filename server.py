from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client

import os
import cred
import requests
import time


chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values.notifications': 2} #2: no notification
chrome_options.add_experimental_option('prefs', prefs)
chrome_path = r'--user-data-dir=/Users/MiaC/Library/Application Support/Google/Chrome/Default'
chrome_options.add_argument(chrome_path)

driver_path = '../../Downloads/chromedriver'
driver = webdriver.Chrome(driver_path, chrome_options = chrome_options)


skuID = '1972827'
product_number = 'P421281'
api_url = f'https://www.sephora.com/api/users/profiles/current/product/{product_number}'
product_url = 'https://www.sephora.com/product/' \
    'artist-face-color-highlight-sculpt-blush-powder-P421281?skuId=1972827'


"""
for testing a product that is in stock.
"""
#skuID = "1972827"
#product_url = "https://www.sephora.com/product/artist-face-color-highlight-sculpt-blush-powder-P421281?skuId=1972868"


def get_skuID_nmuber(product_url):

    return (skuID, product_number)


def signin():
    """
    Sign in to the account.
    The signin form is only triggered by clicking signin again after the drop-down menu shows.
    """

    signin_trigger = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="account_drop_trigger"]/img'))
    )
    signin_trigger.click()
    signin_trigger.click()
     
    #Fill out sign-in info
    id_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="signin_username"]'))
    )
    pw_input = driver.find_element_by_xpath('//*[@id="signin_password"]')
    id_input.send_keys(cred.ACCT)
    pw_input.send_keys(cred.PW)
    driver.find_element_by_xpath('//*[@role="dialog"]/div[1]/form/button').click()


def check_stock(api_url):
    """Check if the product is in stock. """

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    api_res = requests.get(api_url, headers=headers)
    status = api_res.json()
    is_instock = status['regularChildSkus'][0]['actionFlags']['isAddToBasket'] 
    
    return is_instock


def add_to_basket():
    """
    Add to baket and go to shopping cart page.
    Return Boolean. 
    """

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/div[1]/div[2]/div/main/div[1]/div[1]/div[3]/div[3]/div/div/button'
            ))
        ).click()

        print("adding to basket")

        driver.get("https://www.sephora.com/basket")

        return True

    except:
        print("Fail to Add to basket")

def validate_cart(skuID, qty):
    """
    Check if it's the correct product & 
    correct quantity (1) in the shopping cart.
    """

    try:
        print("finding prdocut in cart")
        elem_id = 'qty_' + skuID

        quantity_in_cart= WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, elem_ID))
        ).get_attribute("value")

        if quantity_in_cart == qty:
            return True
        else:
            print("quantity is not correct", quantity_in_cart)

    except:
        print("can't find the product in the cart.")


def check_out():
    """Fill in purchase info"""

    # check out button
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[1]/div/div[2]/button[1]'))
    ).click()

    try:
        # Re-fill password only
        pw_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,'//*[@name="password"]'))
        )

        pw_input.send_keys(cred.PW)

        login_button = driver.find_element_by_xpath(
            '//*[@role="dialog"]/div[1]/form/button'
        ).click()

    except:
        print('Sign in alredy')

    try:
        # CVV
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,'//*[@name="securityCode"]'))
        )
        CVV_input.send_keys(cred.CVV)

        #Save & Continue
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="checkout_section2_body"]/div/div/div[2]/div/div[2]/div[3]/button'
            ))
        )
    except:
        print('Credit Card Saved already')
    finally:
        # alternate_xpath = /html/body/div[1]/div[1]/div/div/main/div/div/div[2]/div/div/div[1]/div[13]/button
        place_order_btn = '/html/body/div[1]/div[1]/div/div/main/div/div/div[2]/div/div/div[1]/div[14]/button'
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, place_order_btn))
        )
        

def send_sms(body):
    account_sid = cred.TWILIO_ACCOUNT_SID
    auth_token = cred.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             body=body,
             from_=cred.FROM,
             to=cred.TO_PHONE
         )


driver.get(product_url)

try:
    signin()
except:
    print("Already signed in")

print("Start to check product status.")

start_time = time.asctime()
print(start_time)
while True :
    try:
        if check_stock(api_url) == True:
            break

    except ConnectionError as e:
        print(e, time.asctime())
        time.sleep(60)
        continue

    

add_to_basket()

if validate_cart(skuID, qty):
    try:
        check_out()
    except:
        body = 'In stock, but fail to check out'
        send_sms(body)
        print("Fail to check out")
    finally:
        body = 'Successfully purchased.'
        send_sms(body)





    





