#id元素定位
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep
dr=webdriver.Chrome()
dr.get("https://mail.qq.com")
dr.implicitly_wait(2)
#dr.maximinze_window()#让窗口最大化
sleep(2)
dr.switch_to.frame(0)
dr.find_element_by_link_text("帐号密码登录").click()
sleep(2)
dr.find_element_by_id("u").send_keys("695362944")

dr.find_element_by_id("p").send_keys("lyp091136216250!")
sleep(2)
dr.find_element_by_id("login_button").click()
sleep(2)
dr.find_element_by_link_text("写信").click()
dr.switch_to.frame('mainFrame')
sleep(5)
dr.find_element_by_xpath("//*[@id='toAreaCtrl']/div[2]/input").send_keys('741881781@qq.com')
dr.find_element_by_xpath("//*[@id='subject']").send_keys('sdf')
a=dr.find_element_by_xpath("//*[@class='qmEditorIfrmEditArea']")
dr.switch_to.frame(a)

dr.find_element(By.XPATH,"/html/body").send_keys("Everything is importable !")
dr.switch_to.parent_frame()
#dr.switch_to.default_content()
sleep(3)
#dr.switch_to.frame('mainFrame')
dr.find_element_by_xpath("//*[@id='toolbar']/div/a[1]").click()
