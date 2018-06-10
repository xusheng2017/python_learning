from selenium import webdriver
import time
import re
from modules.solve_picture import get_data
from selenium.webdriver.chrome.options import Options


def get_start_cookies(user_name, pass_word, tianyan_logger):
    url = 'https://www.tianyancha.com/login'
    while True:
        try:
            # 使用chromheaderless,使用过程会出错,添加异常处理
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)
            time.sleep(5)
            uname = driver.find_element_by_xpath(
                '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input')
            # 输入账号
            uname.send_keys(user_name)
            time.sleep(3)
            pwd = driver.find_element_by_xpath(
                '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input')
            # 输入密码
            pwd.send_keys(pass_word)
            time.sleep(3)
            submit = driver.find_element_by_xpath(
                '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]')
            submit.click()
            # 添加隐式等待,进入天眼查首页
            driver.implicitly_wait(5)
            driver.maximize_window()
            driver.implicitly_wait(3)
            # 请求详情页
            driver.get('http://hefei.tianyancha.com/search')
            driver.implicitly_wait(3)
            # 判断是否有验证码
            if re.match(r'https://antirobot\.tianyancha\.com/captcha/verify', driver.current_url):
                # 如果遇到验证码,关闭之前开启的窗口
                driver.close()
                # 进行打码
                start_cookies = get_data('http://nanjing.tianyancha.com/search', user_name, pass_word, tianyan_logger)[0]
            else:
                list_cookies = driver.get_cookies()
                driver.close()
                start_cookies = {}
                for cookie in list_cookies:
                    start_cookies[cookie['name']] = cookie['value']
                tianyan_logger.info("get cookies sucess!")
            return start_cookies
        except Exception as e:
            tianyan_logger.error("fail to get cookies:{}".format(str(e)))

