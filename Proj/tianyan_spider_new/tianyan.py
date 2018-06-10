import requests
from lxml import etree
import time
import re
from modules.create_log import creat_log
from modules.solve_picture import get_data
from modules.get_start_cookies import get_start_cookies
import pprint
import logging
from modules.deal_mongodb import insert_data

# 用户名,密码(vip)
# 帐号列表
account_number = [{'user_name': '15850512903', 'pass_word': '1qaz2wsx'},
                  {'user_name': '13637079102', 'pass_word': '1qaz2wsx'},
                  {'user_name': '15251883798', 'pass_word': '1qaz2wsx'},
                  {'user_name': '13400062732', 'pass_word': '1qaz2wsx'}
                  ]
# 存储有效帐号
user_name = account_number[1]['user_name']
pass_word = '1qaz2wsx'
# user_name = '17551027266' yes
# pass_word = '1qaz2wsx'
# user_name = '18112128953' yes
# pass_word = '1qaz2wsx'
# -----------------------------------------------------------
# user_name = '18457199821' yes
# pass_word = '1qaz2wsx'
# user_name = '18894583667' yes
# pass_word = '1qaz2wsx'
# user_name = '18751875534' yes
# pass_word = '1qaz2wsx'
# user_name = '15251883798' yes
# pass_word = '1qaz2wsx'
# -----------------------------------------------------------
# user_name = '18014491226' yes
# pass_word = '1qaz2wsx'
# user_name = '18551822797' yes
# pass_word = '1qaz2wsx'
# user_name = '15605151075' yes
# pass_word = '1qaz2wsx'
# user_name = '13584051676' yes
# pass_word = '1qaz2wsx'
# -----------------------------------------------------------
# user_name = '13654429729' yes
# pass_word = '1qaz2wsx'
# user_name = '15902013101' yes
# pass_word = '1qaz2wsx'


tianyan_logger = creat_log()


class TianYan(object):
    def __init__(self, start_cookies):
        self.start_url = 'https://hefei.tianyancha.com/search'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        self.cookies = start_cookies
        # 连接数据库
        # self.conn = connect(host='localhost', port=3306, database='tianyan', user='root', password='mysql', charset='utf8')

    # 发起起始的请求
    def start_request(self):
        response = requests.get(self.start_url, headers=self.headers, cookies=self.cookies)
        if re.match(r'https://antirobot\.tianyancha\.com/captcha/verify', response.url):
            # 进行打码,重新登陆以后需要更新cookie
            self.cookies, html_response = get_data(response.url, user_name, pass_word, tianyan_logger)
        el = etree.HTML(response.content.decode())
        # 获取每个省份每个地区对应的链接地址
        area_dict = dict()
        # 福建地区
        ah_city_url = el.xpath("//div[@id='sc_Content']/div[position()>1]/a/@href")
        tianyan_logger.info('每个城市对应的url{}'.format(ah_city_url))
        ah_city_name = el.xpath("//div[@id='sc_Content']/div[position()>1]/a/text()")
        tianyan_logger.info('每个城市的名字{}'.format(ah_city_name))
        ah_city_list = list()
        for i in range(len(ah_city_url)):
            date = dict()
            date['city_base_url'] = ah_city_url[i]
            date['city'] = ah_city_name[i]
            # 拼接获取每个城市所有的url
            date['url_list'] = list()
            for i in range(1, 251):
                url = date['city_base_url'] + '/p' + str(i)
                date['url_list'].append(url)
            ah_city_list.append(date)
        area_dict['四川'] = ah_city_list
        # 福建地区
        # 广东地区
        tianyan_logger.info('获取所有地区对应的url{}'.format(pprint.pformat(area_dict)))
        return area_dict

    # 发起请求,获取响应
    def get_response(self, area_dict):
        for p, city_list in area_dict.items():
            # 获取省份名字
            province_name = p
            # 遍历每个城市(程序中途如果有问题,查看终止时对应的城市,重新提取,不需要从头开始)
            """
            todo:断点续爬
            """
            for city in city_list[12:]:
                # 添加每个城市所有的公司列表
                city_name = city['city']
                city['company_url_list'] = list()
                # 获取每个城市的相关信息
                for url in city['url_list']:
                    # 发起请求获取每一页的数据,请求两次,如果获取不到响应内容,将url重新添加到请求队列
                    try:
                        response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=3)
                    except:
                        # 第二次请求
                        try:
                            # 第一次获取不到响应可能由于网络原因,添加强制等待,重新发起请求
                            time.sleep(2)
                            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=3)
                        except:
                            city['url_list'].append(url)

                        else:
                            # 判断是否有验证码
                            if re.match(r'https://antirobot\.tianyancha\.com/captcha/verify', response.url):
                                # 进行打码,重新登陆以后需要更新cookie
                                self.cookies, html_response = get_data(response.url, user_name, pass_word, tianyan_logger)
                            else:
                                html_response = response.content.decode()
                            self.parse_page_response(html_response, city['company_url_list'], province_name, city_name)
                            logging.info('--------成功解析当前城市当前页内容:{}--------'.format(city_name))
                    # 如果第一次请求获取响应
                    else:
                        # 判断是否有验证码
                        if re.match(r'https://antirobot\.tianyancha\.com/captcha/verify', response.url):
                            # 进行打码,重新登陆以后需要更新cookie
                            self.cookies, html_response = get_data(response.url, user_name, pass_word, tianyan_logger)
                        else:
                            html_response = response.content.decode()
                        # 解析每一页的响应内容
                        self.parse_page_response(html_response, city['company_url_list'], province_name, city_name)
                        logging.info('--------成功解析当前城市当前页内容:{}--------'.format(city_name))
        # 返回所有结果
        return area_dict

    # 解析每一页的响应内容
    def parse_page_response(self, html_response, company_url_list, province, city):
        global user_name
        global pass_word
        el = etree.HTML(html_response)
        node_list = el.xpath('//div[@class="b-c-white search_result_container"]/div')
        for node in node_list:
            # 获取每家公司对应的url
            company_url = node.xpath('./div[2]/div[1]/a/@href')[0]
            # 公司名字,列表页解析添加数据
            try:
                add_company_name = node.xpath('./div[2]/div[1]/a/span/text()')[0]
            except:
                add_company_name = '未披露'
            try:
                add_register_capital = node.xpath('./div[2]/div[2]/div/div[2]/span/text()')[0]
            except:
                add_register_capital = '未披露'
            try:
                add_register_time = node.xpath('./div[2]/div[2]/div[1]/div[3]/span/text()')[0]
            except:
                add_register_time = '未披露'
            company_url_list.append(company_url)
            time.sleep(3)
            # 发起每家公司的详情页请求
            try:
                response = requests.get(company_url, headers=self.headers, cookies=self.cookies, timeout=3)
            except:
                # 第二次请求
                try:
                    # 第一次获取不到响应可能由于网络原因,添加强制等待,重新发起请求
                    time.sleep(2)
                    response = requests.get(company_url, headers=self.headers, cookies=self.cookies, timeout=3)
                except:
                    pass
                else:
                    # 判断是否有验证码
                    if re.match(r'https://antirobot\.tianyancha\.com/captcha/verify', response.url):
                        # 进行打码,重新登陆以后需要更新cookie
                        self.cookies, html_response = get_data(response.url, user_name, pass_word, tianyan_logger)
                    # 判断是否封号
                    elif response.status_code == 404:
                        # 切换帐号,更新cookie,判断当前帐号是否有效
                        for user in account_number:
                            user_name = user['user_name']
                            pass_word = user['pass_word']
                            self.cookies = get_start_cookies(user_name, pass_word, tianyan_logger)
                            try:
                                response = requests.get(company_url, headers=self.headers, cookies=self.cookies,
                                                        timeout=3)
                            except:
                                try:
                                    response = requests.get(company_url, headers=self.headers, cookies=self.cookies,
                                                            timeout=3)
                                except:
                                    response.status_code = 600
                            if response.status_code == 200:
                                tianyan_logger.info('获取有效帐号{}'.format(pprint.pformat(user)))
                                # 获取响应页内容
                                html_response = response.content.decode()
                                break
                        # 全部遍历完成后如果没有获取有效帐号,那么添加等待时间一个小时
                        if response.status_code != 200:
                            tianyan_logger.error('------------没有有效帐号,正在等待-------------')
                            time.sleep(3600)
                            # 帐号都失效的话,当前请求响应内容丢失
                            pass
                    else:
                        html_response = response.content.decode()
                    try:
                        # 解析每家公司详情页的内容
                        self.parse_company_response(html_response, province, city, company_url, add_register_capital,
                                                add_register_time, add_company_name)
                    except:
                        pass

            # 如果第一次请求获取响应
            else:
                # 判断是否有验证码
                if re.match(r'https://antirobot\.tianyancha\.com/captcha/verify', response.url):
                    # 进行打码,重新登陆以后需要更新cookie
                    self.cookies, html_response = get_data(response.url, user_name, pass_word, tianyan_logger)
                # 判断是否封号
                elif response.status_code == 404:
                    # 切换帐号,更新cookie,判断当前帐号是否有效
                    for user in account_number:
                        user_name = user['user_name']
                        pass_word = user['pass_word']
                        self.cookies = get_start_cookies(user_name, pass_word, tianyan_logger)
                        try:
                            response = requests.get(company_url, headers=self.headers, cookies=self.cookies,
                                                    timeout=3)
                        except:
                            try:
                                response = requests.get(company_url, headers=self.headers, cookies=self.cookies,
                                                        timeout=3)
                            except:
                                response.status_code = 600
                        if response.status_code == 200:
                            tianyan_logger.info('获取有效帐号{}'.format(pprint.pformat(user)))
                            break
                    # 全部遍历完成后如果没有获取有效帐号,那么添加等待时间一个小时
                    if response.status_code != 200:
                        tianyan_logger.error('------------没有有效帐号,正在等待-------------')
                        time.sleep(3600)
                        # 帐号都失效的话,当前请求响应内容丢失
                        pass
                    # 获取响应页内容
                    html_response = response.content.decode()
                else:
                    html_response = response.content.decode()
                try:
                    # 解析响应内容,获取每家公司的详情页
                    self.parse_company_response(html_response, province, city, company_url, add_register_capital,
                                                add_register_time, add_company_name)
                except:
                    # 解析每家公司详情页内容出错,重新添加到请求列表中
                    pass

    # 解析每一家公司的详情页内容,
    def parse_company_response(self, html_response, province, city, company_url, add_register_capital,
                               add_register_time, add_company_name):
        el = etree.HTML(html_response)
        company_web_top = dict()
        try:
            # 获取基础信息
            company_web_top['company_name'] = el.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[1]/h1/text()')[0]
        except:
            company_web_top['company_name'] = '未披露'
        try:
            company_web_top['tel'] = el.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[2]/div[1]/span[2]/text()')[0]
        except:
            company_web_top['tel'] = '未披露'
        try:
            company_web_top['email'] = el.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[2]/div[2]/span[2]/text()')[0]
        except:
            company_web_top['email'] = '未披露'
        try:
            company_web_top['company_url'] = el.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[3]/div[1]/a/text()')[0]
        except:
            company_web_top['company_url'] = '未披露'
        try:
            company_web_top['addr'] = el.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[3]/div[2]/span[2]/text()')[0]
        except:
            company_web_top['addr'] = '未披露'
        tianyan_logger.info('--------获取公司基础信息:{}--------'.format(company_web_top['company_name']))

        # 获取工商信息
        basic_info = dict()
        try:
            basic_info['legal_person'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[2]/table/tbody/tr/td[1]/div/div[1]/div[2]/div/a/text()')[0]
        except:
            basic_info['legal_person'] = '未披露'
        try:
            basic_info['register_capital'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[2]/table/tbody/tr/td[2]/div[1]/div[2]/div/text/text()')[0]
        except:
            basic_info['register_capital'] = '未披露'
        try:
            basic_info['register_time'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[2]/table/tbody/tr/td[2]/div[2]/div[2]/div/text/text()')[0]
        except:
            basic_info['register_time'] = '未披露'
        try:
            # 公司状态
            basic_info['company_status'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[2]/table/tbody/tr/td[2]/div[3]/div[2]/div/text()')[0]
        except:
            basic_info['company_status'] = '未披露'
        try:
            basic_info['brn'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[1]/td[2]/text()')[0]
        except:
            basic_info['brn'] = '未披露'
        try:
            basic_info['organization_code'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[1]/td[4]/text()')[0]
        except:
            basic_info['organization_code'] = '未披露'
        try:
            # 统一信用代码
            basic_info['ucc'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[2]/td[2]/text()')[0]
        except:
            basic_info['ucc'] = '未披露'
        try:
            basic_info['company_type'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[2]/td[4]/text()')[0]
        except:
            basic_info['company_type'] = '未披露'
        try:
            # 纳税人识别号
            basic_info['tln'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[3]/td[2]/text()')[0]
        except:
            basic_info['tln'] = '未披露'
        try:
            basic_info['industry'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[3]/td[4]/text()')[0]
        except:
            basic_info['industry'] = '未披露'
        try:
            # 营业时间
            basic_info['operating_period'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[4]/td[2]/span/text()')[0]
        except:
            basic_info['operating_period'] = '未披露'
        try:
            # 核准日期
            basic_info['approval_date'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[4]/td[4]/text/text()')[0]
        except:
            basic_info['approval_date'] = '未披露'
        try:
            basic_info['register_authority'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[5]/td[2]/text()')[0]
        except:
            basic_info['register_authority'] = '未披露'
        try:
            basic_info['english_name'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[5]/td[4]/text()')[0]
        except:
            basic_info['english_name'] = '未披露'
        try:
            basic_info['register_addr'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[6]/td[2]/text()')[0]
        except:
            basic_info['register_addr'] = '未披露'
        try:
            # 经营范围
            basic_info['business_scope'] = el.xpath('//*[@id="_container_baseInfo"]/div/div[3]/table/tbody/tr[7]/td[2]/span/span/span[@class="js-full-container hidden"]/text()')[0]
        except:
            basic_info['business_scope'] = '未披露'
        tianyan_logger.info('--------获取公司工商信息--------')

        # 主要成员
        member_list = list()
        members = el.xpath('//*[@id="_container_staff"]/div/div[1]/div')
        for member in members:
            member_info = dict()
            try:
                # 职位
                member_info['position'] = member.xpath('./div/div[1]/span/text()')[0]
            except:
                member_info['position'] = '未披露'
            try:
                # 姓名
                member_info['name'] = member.xpath('./div/a/text()')[0]
            except:
                member_info['name'] = '未披露'
            member_list.append(member_info)
        tianyan_logger.info('--------获取公司成员及职位--------')

        # 股东信息
        shareholder_list = list()
        shareholders = el.xpath('//*[@id="_container_holder"]/div/table/tbody/tr')
        for shareholder in shareholders:
            shareholder_info = dict()
            try:
                shareholder_info['name'] = shareholder.xpath('./td[1]/a/text()')[0]
            except:
                shareholder_info['name'] = '未披露'
            try:
                shareholder_info['proportion'] = shareholder.xpath('./td[2]/div/div/span/text()')[0]
            except:
                shareholder_info['proportion'] = '未披露'
            try:
                shareholder_info['Investment'] = shareholder.xpath('./td[3]/div/span[1]/text()')[0]
            except:
                shareholder_info['Investment'] = '未披露'
            try:
                shareholder_info['time'] = shareholder.xpath('./td[3]/div/span[2]/text()')[0]
            except:
                shareholder_info['time'] = '未披露'
            shareholder_list.append(shareholder_info)
        tianyan_logger.info('--------获取公司股东信息--------')

        # 融资记录
        finance_history_list = list()
        finance_historys = el.xpath('//*[@id="_container_rongzi"]/div/div/table/tbody/tr')
        for finance_history in finance_historys:
            finance_history_info = dict()
            try:
                # 时间
                finance_history_info['time'] = finance_history.xpath('./td[1]/span/text()')[0]
            except:
                finance_history_info['time'] = '未披露'
            try:
                # 轮次
                finance_history_info['rounds'] = finance_history.xpath('./td[2]/span/text()')[0]
            except:
                finance_history_info['rounds'] = '未披露'
            try:
                # 估值
                finance_history_info['valuation'] = finance_history.xpath('./td[3]/span/text()')[0]
            except:
                finance_history_info['valuation'] = '未披露'
            try:
                # 金额
                finance_history_info['amount'] = finance_history.xpath('./td[4]/span/text()')[0]
            except:
                finance_history_info['amount'] = '未披露'
            try:
                # 比例
                finance_history_info['proportion'] = finance_history.xpath('./td[5]/span/text()')[0]
            except:
                finance_history_info['proportion'] = '未披露'
            try:
                # 投资方
                finance_history_info['investor'] = finance_history.xpath('./td[6]/span/text()')[0]
            except:
                finance_history_info['investor'] = '未披露'
            finance_history_list.append(finance_history_info)
        tianyan_logger.info('--------获取公司融资历史--------')

        # 最近变更记录
        change_log_list = list()
        change_logs = el.xpath('//*[@id="_container_changeinfo"]/div/div[1]/table/tbody/tr')
        for change_log in change_logs:
            change_log_info = dict()
            try:
                # 时间
                change_log_info['time'] = change_log.xpath('./td[1]/div/text()')[0]
            except:
                change_log_info['time'] = '未披露'
            try:
                # 项目
                change_log_info['project'] = change_log.xpath('./td[2]/div/text()')[0]
            except:
                change_log_info['project'] = '未披露'
            try:
                # 变更前
                change_log_info['pro'] = change_log.xpath('./td[3]/div/text()')[0]
            except:
                change_log_info['pro'] = '未披露'
            try:
                # 变更后
                change_log_info['after'] = change_log.xpath('./td[4]/div/text()')[0]
            except:
                change_log_info['after'] = '未披露'
            change_log_list.append(change_log_info)
        tianyan_logger.info('--------获取企业变更记录--------')

        # 法律诉讼
        legal_proceeding_list = list()
        legal_proceedings = el.xpath('//*[@id="_container_lawsuit"]/div/div[1]/table/tbody/tr')
        for legal_proceeding in legal_proceedings:
            legal_proceedings_info = dict()
            try:
                # 时间
                legal_proceedings_info['time'] = legal_proceeding.xpath('./td[1]/span/text()')[0]
            except:
                legal_proceedings_info['time'] = '未披露'
            try:
                # 判决文书
                legal_proceedings_info['judgments'] = legal_proceeding.xpath('./td[2]/a/text()')[0]
            except:
                legal_proceedings_info['judgments'] = '未披露'
            try:
                # 判决文书对应的url
                legal_proceedings_info['url'] = legal_proceeding.xpath('./td[2]/a/@href')[0]
            except:
                legal_proceedings_info['url'] = '未披露'
            try:
                # 案由
                legal_proceedings_info['case'] = legal_proceeding.xpath('./td[3]/span/text()')[0]
            except:
                legal_proceedings_info['case'] = '未披露'
            try:
                # 案件身份
                legal_proceedings_info['identity'] = legal_proceeding.xpath('./td[4]/div/text()')[0]
            except:
                legal_proceedings_info['identity'] = '未披露'
            try:
                # 案件号
                legal_proceedings_info['port'] = legal_proceeding.xpath('./td[5]/span/text()')[0]
            except:
                legal_proceedings_info['port'] = '未披露'
            legal_proceeding_list.append(legal_proceedings_info)
        tianyan_logger.info('--------获取公司法律诉讼记录--------')

        # 法院公告
        court_notice_list = list()
        court_notices = el.xpath('//*[@id="_container_court"]/div/div[1]/table/tbody/tr')
        for court_notice in court_notices:
            court_notice_info = dict()
            try:
                # 时间
                court_notice_info['time'] = court_notice.xpath('./td[1]/text()')[0]
            except:
                court_notice_info['time'] = '未披露'
            try:
                # 上诉方
                court_notice_info['appealant'] = court_notice.xpath('./td[2]/span/a/text()')[0]
            except:
                court_notice_info['appealant'] = '未披露'
            try:
                # 被诉方
                court_notice_info['accused'] = court_notice.xpath('./td[3]/span/text()')[0]
            except:
                court_notice_info['accused'] = '未披露'
            try:
                # 公告类型
                court_notice_info['type'] = court_notice.xpath('./td[4]/span/text()')[0]
            except:
                court_notice_info['type'] = '未披露'
            try:
                # 法院
                court_notice_info['court'] = court_notice.xpath('./td[5]/script/text()')[0]
            except:
                court_notice_info['court'] = '未披露'
            try:
                # 公告
                court_notice_info['detail'] = court_notice.xpath('./td[6]/script/text()')[0]
            except:
                court_notice_info['detail'] = '未披露'
            court_notice_list.append(court_notice_info)
        tianyan_logger.info('--------获取公司法院公告--------')

        # 行政处罚
        announce_list = list()
        announces = el.xpath('//*[@id="_container_punish"]/div/div[1]/table/tbody/tr')
        for announce in announces:
            announce_info = dict()
            try:
                # 时间
                announce_info['time'] = announce.xpath('./td[1]/span/text()')[0]
            except:
                announce_info['time'] = '未披露'
            try:
                # 决定文号
                announce_info['port'] = announce.xpath('./td[2]/span/text()')[0]
            except:
                announce_info['port'] = '未披露'
            try:
                # 决定机关
                announce_info['organ'] = announce.xpath('./td[4]/div/text()')[0]
            except:
                announce_info['organ'] = '未披露'
            try:
                # 详情
                announce_info['detail'] = announce.xpath('./td[5]/script/text()')[0]
            except:
                announce_info['detail'] = '未披露'
            announce_list.append(announce_info)
        tianyan_logger.info('--------获取公司行政处罚--------')

        # 公司的详情内容
        company = dict()
        company['company_url'] = company_url
        company['province'] = province
        company['city'] = city
        # 额外添加注册资本和注册时间以及公司名字
        company['add_register_capital'] = add_register_capital
        company['add_register_time'] = add_register_time
        company['add_company_name'] = add_company_name

        company['company_web_top'] = company_web_top
        company['basic_info'] = basic_info
        company['member_list'] = member_list
        company['shareholder_list'] = shareholder_list
        company['finance_history_list'] = finance_history_list
        company['change_log_list'] = change_log_list
        company['legal_proceeding_list'] = legal_proceeding_list
        company['court_notice_list'] = court_notice_list
        company['announce_list'] = announce_list
        # 数据进行存储
        insert_data(company, tianyan_logger)
        tianyan_logger.info('----------成功获取公司详细信息:{}------------'.format(city))

    def run(self):
        area_dict = self.start_request()
        self.get_response(area_dict)


if __name__ == '__main__':
    # 获取起始的cookies
    start_cookies = get_start_cookies(user_name, pass_word, tianyan_logger)
    tianyan_logger.info('第一次登陆后提取的cookie{}'.format(pprint.pformat(start_cookies)))
    tianyan = TianYan(start_cookies)
    tianyan.run()
    tianyan_logger.info('------------finish to get data------------')

