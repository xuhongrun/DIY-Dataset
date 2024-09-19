from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions


class JD:
    def __init__(self) -> None:
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')
        self.driver = webdriver.Chrome(options=option)

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
        pass

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

        goods = self.driver.find_elements(By.CSS_SELECTOR, '.gl-item')
        for good in goods:
            good_data = {}

            is_self_operated = False
            try:
                good.find_element(By.CSS_SELECTOR, '.p-name > span')
                is_self_operated = True
            except:
                is_self_operated = False
            price = good.find_element(By.CSS_SELECTOR, '.p-price').text
            image = good.find_element(By.CSS_SELECTOR, '.p-img a img').get_attribute('src')
            title = good.find_element(By.CSS_SELECTOR, '.p-name a em').text.replace(r'\n', '')
            link = good.find_element(By.CSS_SELECTOR, '.p-name a').get_attribute('href')
            detail = self.__detail(str(link))

            print('自营：'+str(is_self_operated))
            print('名称：'+str(title))
            print('图片：'+str(image))
            print('价格：'+str(price))
            print('链接：'+str(link))
            print('参数：\n'+detail)
            print('*'*20)

            good_data['is_self_operated'] = is_self_operated
            good_data['name'] = str(title)
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
