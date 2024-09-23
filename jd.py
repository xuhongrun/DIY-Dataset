#!/usr/bin/python

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import requests
from PIL import Image
import cv2
import numpy as np
from io import *


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

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'key'))
        )

    # TODO
    def verificationCode(self):
        # 等待验证码加载
        bg_img_element = self.driver.find_element_by_xpath('//div[@class="JDJRV-bigimg"]/img')
        bg_img_src = bg_img_element.get_attribute('src')

        # 下载并处理验证码图片
        response = requests.get(bg_img_src)
        bg_img = Image.open(BytesIO(response.content))
        bg_img = bg_img.convert('RGBA')

        # 转换为OpenCV格式
        bg_img_cv = np.array(bg_img)
        bg_img_gray = cv2.cvtColor(bg_img_cv, cv2.COLOR_BGR2GRAY)

        # 等待滑块图片加载
        slider_img_element = self.driver.find_element_by_xpath('//div[@class="JDJRV-smallimg"]/img')
        slider_img_src = slider_img_element.get_attribute('src')

        # 下载滑块图片
        response = requests.get(slider_img_src)
        slider_img = Image.open(BytesIO(response.content))
        slider_img = slider_img.convert('RGBA')

        # 转换为OpenCV格式
        slider_img_cv = np.array(slider_img)
        slider_img_gray = cv2.cvtColor(slider_img_cv, cv2.COLOR_BGR2GRAY)

        # 使用模板匹配找到滑块位置
        result = cv2.matchTemplate(bg_img_gray, slider_img_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 计算滑块需要滑动的距离
        slider_distance = max_loc[0] - slider_img.size[0] / 2

        # 执行滑动操作
        slider_element = self.driver.find_element_by_xpath('//div[@class="JDJRV-slide-btn"]')
        actions = ActionChains(self.driver)
        actions.click_and_hold(slider_element).perform()
        actions.move_by_offset(slider_distance, 0).perform()
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
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.gl-item'))
        )

        # scroll
        for i in range(10):
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
                brand = re.match(r'品牌：([\d\w\(\)\（\）\-\_ \u4e00-\u9fa5]*)', detail).group(1).strip()
                print(brand)
                product_name = re.match(r'商品名称：([\d\w\(\)\（\）\-\_ \u4e00-\u9fa5]*)', detail).group(1).strip()
                print(product_name)
            except Exception as e:
                print('Error brand product_name !!! %s' % e)

            print('自营：'+str(is_self_operated))
            print('品牌：'+str(brand))
            print('商品名称：'+str(product_name))
            print('图片：'+str(image))
            print('价格：'+str(price))
            print('链接：'+str(link))
            print('参数：\n'+detail)
            print('*'*20)

            good_data['is_self_operated'] = is_self_operated
            good_data['brand'] = str(brand)
            good_data['name'] = str(title)
            good_data['product_name'] = str(product_name)
            good_data['image'] = str(image)
            good_data['price'] = str(price)
            good_data['link'] = str(link)
            good_data['detail'] = detail

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
