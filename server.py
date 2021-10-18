

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cred


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2} #2: no notification
chrome_options.add_experimental_option("prefs", prefs)
driver_path = "../../Downloads/chromedriver"
driver = webdriver.Chrome(driver_path, chrome_options = chrome_options)
product_url = "https://www.sephora.com/product/artist-face-color-highlight-sculpt-blush-powder-P421281?skuId=1972827&%24deep_link=true&om_mmc=tr-us_3b36fd97-04e6-477e-9dea-e52daedcb029-he-ppage-ROUGE&emtc2=3b36fd97-04e6-477e-9dea-e52daedcb029&emcampaign=US_Back_In_Stock_DRTM&emlid=df2e66452b164cd8b1bcb73c53bef3a0&emaid&ematg=7376018366&emcid=52086441&promo&viq_epid=e079ac2f-379d-4e29-847b-5c160b46eb19%7C52086441&%243p=e_ep&_branch_match_id=932635593685137435&utm_medium=Email%20Epsilon"

"""Sign in process"""
driver.get(product_url)

signin_menu = driver.find_element_by_id('account_drop_trigger')
signin_submenu = driver.find_element_by_xpath('//*[@id="account_drop"]/div[1]/div/div[2]/button[1]')
LoginChains = webdriver.ActionChains
LoginChains(driver).move_to_element(signin_menu).click(signin_submenu).perform()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signin_username"]')))
id_input = driver.find_element_by_xpath('//*[@id="signin_username"]')
pw_input = driver.find_element_by_xpath('//*[@id="signin_password"]')

id_input.send_keys(cred.ACCT)
pw_input.send_keys(cred.PW)

login_button = driver.find_element_by_xpath('//*[@id="modal1Dialog"]/div[1]/form/button').click()


"""Check if it's in stock"""



"""Add to baket"""


"""Fill in purchase info"""




