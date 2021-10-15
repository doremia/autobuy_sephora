

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver_path = "../../Downloads/chromedriver"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2} #2: no notification
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(driver_path, chrome_options = chrome_options)
product_url = "https://www.sephora.com/product/artist-face-color-highlight-sculpt-blush-powder-P421281?skuId=1972827&%24deep_link=true&om_mmc=tr-us_3b36fd97-04e6-477e-9dea-e52daedcb029-he-ppage-ROUGE&emtc2=3b36fd97-04e6-477e-9dea-e52daedcb029&emcampaign=US_Back_In_Stock_DRTM&emlid=df2e66452b164cd8b1bcb73c53bef3a0&emaid&ematg=7376018366&emcid=52086441&promo&viq_epid=e079ac2f-379d-4e29-847b-5c160b46eb19%7C52086441&%243p=e_ep&_branch_match_id=932635593685137435&utm_medium=Email%20Epsilon"
driver.get(product_url)




