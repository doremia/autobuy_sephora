from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cred
import requests
import time

chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values.notifications': 2} #2: no notification
chrome_options.add_experimental_option('prefs', prefs)
chrome_path = r'--user-data-dir=/Users/MiaC/Library/Application Support/Google/Chrome/Default'
# or /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
chrome_options.add_argument(chrome_path)

driver_path = '../../Downloads/chromedriver'
driver = webdriver.Chrome(driver_path, chrome_options = chrome_options)

skuID = "1972868"
#skuID = "1972827"
# product_url = 'https://www.sephora.com/product/artist-face-color-highlight-sculpt-blush-powder-P421281?skuId=1972827&%24deep_link=true&om_mmc=tr-us_3b36fd97-04e6-477e-9dea-e52daedcb029-he-ppage-ROUGE&emtc2=3b36fd97-04e6-477e-9dea-e52daedcb029&emcampaign=US_Back_In_Stock_DRTM&emlid=df2e66452b164cd8b1bcb73c53bef3a0&emaid&ematg=7376018366&emcid=52086441&promo&viq_epid=e079ac2f-379d-4e29-847b-5c160b46eb19%7C52086441&%243p=e_ep&_branch_match_id=932635593685137435&utm_medium=Email%20Epsilon'
product_url = 'https://www.sephora.com/product/artist-face-color-highlight-sculpt-blush-powder-P421281?skuId=1972868&%24deep_link=true&om_mmc=tr-us_3b36fd97-04e6-477e-9dea-e52daedcb029-he-ppage-ROUGE&emtc2=3b36fd97-04e6-477e-9dea-e52daedcb029&emcampaign=US_Back_In_Stock_DRTM&emlid=df2e66452b164cd8b1bcb73c53bef3a0&ematg=7376018366&emcid=52086441&viq_epid=e079ac2f-379d-4e29-847b-5c160b46eb19|52086441&%243p=e_ep&_branch_match_id=932635593685137435&utm_medium=Email%20Epsilon'
# driver.get(product_url)
driver.get("https://www.sephora.com/basket")

def signin():
    """Sign in to the account.
        The signin form is only triggered by clicking signin again after the drop-down menu shows.
    """

    signin_menu = driver.find_element_by_id('account_drop_trigger')
    signin_trigger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="account_drop_trigger"]/img')))
    # LoginChains = webdriver.ActionChains
    # LoginChains(driver).click(signin_menu).click(signin_trigger).perform()
    signin_trigger.click()
    signin_trigger.click()
     

    id_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signin_username"]')))
    pw_input = driver.find_element_by_xpath('//*[@id="signin_password"]')
    id_input.send_keys(cred.ACCT)
    pw_input.send_keys(cred.PW)

    login_button = driver.find_element_by_xpath('//*[@role="dialog"]/div[1]/form/button').click()


def check_stock():
    """Check if the product is in stock. """

    api_url = 'https://www.sephora.com/api/users/profiles/current/product/P421281'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    api_res = requests.get(api_url, headers=headers)
    status = api_res.json()
    is_instock = status['regularChildSkus'][1]['actionFlags']['isAddToBasket']

    print(is_instock)

    return is_instock


def add_to_basket():
    """
    Add to baket and go to shopping cart page.
    Return Boolean. 
    """

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div/main/div[1]/div[1]/div[3]/div[3]/div/div/button'))).click()
        print("adding to basket")
        driver.get("https://www.sephora.com/basket")

        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[role="dialog"]/div[2]/div[1]/div[2]/div[2]/a'))).click()
        # print("get to shopping cart")
        return True

    except:
        print("Fail to Add to basket")

def validate_cart(skuID):

    try:
        quantity = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, skuID))).get_attribute("value")

        return quantity

    except:
        print("can't find the product in the cart.")


def check_out():
    """Fill in purchase info"""

    # check out button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div/div/main/div/div/div[2]/div[1]/div/div[2]/button[1]'))).click()

    # Re-fill password only
    pw_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@name="password"]')))
    pw_input.send_keys(cred.PW)

    login_button = driver.find_element_by_xpath('//*[@role="dialog"]/div[1]/form/button').click()

    # CVV
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@name="securityCode"]')))
    CVV_input.send_keys(cred.CVV)

    #Save & Continue
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="checkout_section2_body"]/div/div/div[2]/div/div[2]/div[3]/button')))

    #Place order btn
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div/div/main/div/div/div[2]/div/div/div[1]/div[14]/button')))




try:
    signin()
except:
    print("Already signed in")

# attempt = 1
# while check_stock() != True :
#     print("sold out")
    
#     print(f"this is the {attempt}th attempt")
#     attempt += 1

#     time.sleep(3)


# add_to_basket()


if validate_cart("qty_1972868") == 1:
    check_out()
    





