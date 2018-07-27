from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from modules.rk import *
import re
import base64
import pprint


# 进行打码
def get_data(verify_url, user_name, pass_word, tianyan_logger):
    while True:
        # 模拟登陆
        url = 'https://www.tianyancha.com/login'
        try:
            # 使用chromheaderless
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            # 打码过程中,由于网络原因可能会出错
            # 连接打码兔平台，返回要点击的坐标
            # 查看是否还有余额
            money = rc.rk_demand()
            tianyan_logger.info('打码兔剩余的分数:{}'.format(money))
            # 如果有钱，进行打码
            if int(money) > 100:
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
                time.sleep(1)
                # 对验证码页发起请求
                driver.get(verify_url)
                driver.implicitly_wait(5)
                time.sleep(3)
                # 定位节点获取图片截图
                # 上面图片节点
                el_img1 = driver.find_element_by_id("targetImgie")
                # 下面图片节点
                el_img2 = driver.find_element_by_id("bgImgie")
                # 提交按钮节点
                el_sub = driver.find_element_by_id("submitie")

                src1 = el_img1.get_attribute('src')
                src2 = el_img2.get_attribute('src')
                # xpath定位获取的节点内容,将换行符替换为%0A
                src1_data = src1.split(',')[1].replace("%0A", "")
                src2_data = src2.split(',')[1].replace("%0A", "")
                src1_bytes = base64.b64decode(src1_data)
                tianyan_logger.info('-----------------get_base_decode_1-----------------------')
                src2_bytes = base64.b64decode(src2_data)
                tianyan_logger.info('-----------------get_base_decode_2-----------------------')
                with open('img_up.png', 'wb') as f:
                    f.write(src1_bytes)
                # 下载验证码下部分图片
                with open('img_down.png', 'wb') as f:
                    f.write(src2_bytes)
                time.sleep(1)
                # 拼接上下两张图片
                im = Image.open('img_up.png')

                im2 = Image.open('img_down.png')

                im3 = Image.open('tips.png')

                width, height = im.size

                width2, height2 = im2.size

                width3, height3 = im3.size

                result = Image.new(im2.mode, (width, height+height2+height3), '#fff')
                tianyan_logger.info('---------------合成图片-------------------')
                result.paste(im2, box=(0, 0))

                result.paste(im3, box=(0, height2))

                result.paste(im, box=(0, height2+height3))
                result.save('result.png')
                time.sleep(1)
                tianyan_logger.info('-------------生成合成图片并进行打码-----------------')
                # score = dmt.decode('result.png', 308)
                im = open('result.png', 'rb').read()
                score = rc.rk_create(im, 6900)
                tianyan_logger.info(score)
                id = score['Id']
                # 检测返回是否异常，异常上报异常
                # 获取返回的坐标
                target = score['Result']
                tar_list = target.split('.')
                new_tar_list = []
                for tar in tar_list:
                    tar = tar.split(',')
                    new_tar_list.append(tar)
                # 模拟顺序点击
                time.sleep(1)
                actions = ActionChains(driver)
                for i in range(len(new_tar_list)):
                    actions.move_to_element_with_offset(el_img2, new_tar_list[i][0], new_tar_list[i][1])
                    actions.click()
                    actions.perform()
                    time.sleep(2)
                actions.move_to_element(el_sub)
                actions.click()
                actions.perform()
                time.sleep(3)
                driver.implicitly_wait(4)
                if re.search(r'https://antirobot\.tianyancha\.com/captcha/verify\?', driver.current_url):
                    # 上报验证码错误
                    rc.rk_report_error(id)
                    tianyan_logger.info('验证没有通过')
                    driver.close()
                    # 验证码没有通过,等待10秒,重新发送请求再次进行验证
                # elif re.search(r'src="https://static\.tianyancha\.com/web-require-js/themes/18blue/images/404-blue\.jpg"\?', driver.page_source)
                # 验证码识别成功后有可能响应页面是404,如果不作处理,会丢失一条公司数据,当下一次请求时响应内容是404会进行帐号切换
                else:
                    # 验证码通过以后需要更新cookie
                    tianyan_logger.info('验证通过')
                    list_cookies = driver.get_cookies()
                    # 利用这个新的cookie和requests去请求
                    cookies = {}
                    for cookie in list_cookies:
                        cookies[cookie['name']] = cookie['value']
                    source = driver.page_source
                    driver.quit()
                    return cookies, source
            # 没钱了,添加等待,进行充值
            else:
                tianyan_logger.info('#########################打码平台题分已经用完,请充值！#####################')
                time.sleep(600)
        # 打码过程只要出现错误,添加等待2秒,重新进行请求
        except Exception as e:
            print('------- 打码过程错误{}------'.format(str(e)))
            try:
                # 打码过程中如果出错,关闭创建的webdriver实例
                driver.close()
            except:
                pass
            time.sleep(2)


