#!/usr/bin/python

from io import *
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import numpy as np


class JD:
    def __init__(self) -> None:
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        option.add_argument("--log-level=1")
        option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=option)

        self.driver.implicitly_wait(5)

    def __del__(self) -> None:
        self.driver.quit()

    def login(self, user_name: str, pass_word: str):
        # 访问登录页面
        self.driver.get("https://passport.jd.com/new/login.aspx")

        # 填写用户名和密码
        username_input = self.driver.find_element(By.ID, 'loginname')
        password_input = self.driver.find_element(By.ID, 'nloginpwd')

        username_input.send_keys(user_name)
        password_input.send_keys(pass_word)

        # 提交登录表单
        submit_button = self.driver.find_element(By.ID, 'loginsubmit')
        submit_button.click()

        # TODO 图片验证
        # self.verificationCode()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'key'))
        )

    def verificationCode(self):
        # 等待验证码出现
        captcha_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="JDJRV-bigimg"]/img'))
        )

        # 获取验证码图片
        captcha_img = captcha_element.get_attribute("src")
        captcha_img = cv2.imdecode(np.frombuffer(captcha_img.encode("utf-8"), np.uint8), cv2.IMREAD_COLOR)

        # 图像预处理
        gray = cv2.cvtColor(np.array(captcha_img), cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # 寻找滑块
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 50:
                slider_x = x
                slider_y = y
                break

        # 计算滑块的移动距离
        move_distance = slider_x + w - 10

        # 创建ActionChains对象
        actions = ActionChains(self.driver)

        # 点击滑块
        slider_element = self.driver.find_element(By.ID, "slider")
        actions.click_and_hold(slider_element).perform()

        # 移动滑块
        actions.move_by_offset(move_distance, 0).perform()

        # 释放滑块
        actions.release().perform()

    def search(self, keyword: str):
        data = []

        # 访问京东搜索页面
        self.driver.get("https://www.jd.com")

        # 搜索
        search_box = self.driver.find_element(By.ID, 'key')
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.gl-item'))
        )

        # scroll
        for i in range(1):
            self.driver.execute_script(f'document.documentElement.scrollTop={(i+1)*1000}')

        goods = self.driver.find_elements(By.CSS_SELECTOR, '.gl-item')
        for good in goods:
            good_data = {}

            is_self_operated = False
            brand = ''
            product_name = ''
            image = ''
            price = ''
            link = ''
            detail = ''
            try:
                good.find_element(By.CSS_SELECTOR, '.p-name > span')
                is_self_operated = True
            except:
                is_self_operated = False
            price = good.find_element(By.CSS_SELECTOR, '.p-price').text[1:]
            image = good.find_element(By.CSS_SELECTOR, '.p-img a img').get_attribute('src')
            title = good.find_element(By.CSS_SELECTOR, '.p-name a em').text.replace(r'\n', '')
            link = good.find_element(By.CSS_SELECTOR, '.p-name a').get_attribute('href')
            detail = self.__detail(str(link))


            try:
                detail_match = re.match(r'品牌：([：\d\w\(\)\（\）\-\_\/\\ \u4e00-\u9fa5]*)\n商品名称：([\d\w\(\)\（\）\-\_\/\\ \u4e00-\u9fa5]*)\n商品编号：(\d*)\n', detail)

                brand = detail_match.group(1).strip()
                product_name = detail_match.group(2).strip()
                product_number = detail_match.group(3).strip()
            except Exception as e:
                print('Error brand product_name product_number !!! %s' % e)

            good_data['is_self_operated'] = is_self_operated
            good_data['brand'] = str(brand)
            good_data['name'] = str(title)
            good_data['product_name'] = str(product_name)
            good_data['product_number'] = str(product_number)
            good_data['image'] = str(image)
            good_data['price'] = str(price)
            good_data['link'] = str(link)
            good_data['detail'] = detail

            # print(good_data)
            # print('*'*20)

            data.append(good_data)

        return data

    def __detail(self,url: str):
        # 保存当前窗口句柄
        current_window = self.driver.current_window_handle

        # 打开新标签页
        self.driver.execute_script("window.open('');")

        # 等待新标签页加载
        self.driver.implicitly_wait(2)

        # 获取所有窗口句柄
        windows = self.driver.window_handles

        # 切换到新标签页
        new_window = [window for window in windows if window != current_window][0]
        self.driver.switch_to.window(new_window)

        # 在新标签页中打开URL
        self.driver.get(url)

        # 执行操作
        detail = self.driver.find_element(By.CSS_SELECTOR, '.p-parameter').text

        # 关闭新标签页
        self.driver.close()

        # 切换回原始标签页
        self.driver.switch_to.window(current_window)

        return detail
