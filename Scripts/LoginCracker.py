import requests, json
from selenium import common
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time

class LoginCracker:

    def __init__(self, username, password, driver, wait, progress_bar, style):
        self.login_url = "https://accounts.douban.com/passport/login"
        self.driver = driver
        self.wait = wait
        self.username = username
        self.password = password
        self.actual_block_width = 50
        self.progress_bar = progress_bar
        self.style = style

    def login_with_captcha(self):
        try:
            # 步骤一：获得拼图块
            block_top, block_left, block_width = self.get_captcha(self.driver, self.wait, "slideBlock")

            # 步骤二：获得背景图
            slideBkg = self.get_captcha(self.driver, self.wait, "slideBkg", block_top, block_left, block_width)

            # 步骤三：获得的缺口处的左边距 + 拼块的右空白间隙 = 要移动的距离
            distance = self.get_distance(slideBkg) + self.actual_block_width + (
                    block_width - self.actual_block_width) / 2

            # 步骤四：模拟人的行为习惯(先匀加速拖动后匀减速拖动)
            tracks = self.get_tracks(distance)

            # 步骤五：按照轨迹拖动，验证成功
            drag_button = self.wait.until(EC.presence_of_element_located((By.ID, 'tcaptcha_drag_button')))
            ActionChains(self.driver).click_and_hold(drag_button).perform()
            for track in tracks:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

            time.sleep(0.1)  # 0.1秒后释放鼠标
            ActionChains(self.driver).release().perform()

            # 此处等待是为了 POST 请求传输成功，成功后会跳转到账户主页面
            try:
                time.sleep(3)
                self.driver.find_element_by_id("slideBlock")
                self.login_with_captcha()
            except common.exceptions.NoSuchElementException:
                self.driver.switch_to.default_content()
                self.progress_bar['value'] = 20
                self.style.configure("green.Horizontal.TProgressbar", text="20%")
                return "识破验证码，已登录。"
        except:
            self.driver.refresh()
            self.login()

    def click_submit(self):
        try:
            login_by_password = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-tab-account")))
            login_by_password.click()

            input_username = self.driver.find_element_by_id('username')
            input_password = self.driver.find_element_by_id('password')

            input_username.send_keys(self.username)
            input_password.send_keys(self.password)
            submit_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "登录豆瓣")))
            submit_button.click()
        except common.exceptions.NoSuchElementException:
            self.driver.refresh()
            self.click_submit()
        except common.exceptions.TimeoutException:
            return "豆瓣可能检测到你的行为！稍等片刻，请勿多次尝试。"
        try:
            popup_frame = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
            self.driver.switch_to.frame(popup_frame)
            time.sleep(3)
            self.driver.find_element_by_id("slideBlock")
            return self.login_with_captcha()
        except common.exceptions.NoSuchElementException:
            try:
                self.driver.find_element_by_id("capImg")
            except common.exceptions.NoSuchElementException:
                self.progress_bar['value'] = 20
                self.style.configure("green.Horizontal.TProgressbar", text="20%")
                return "跳过验证码，已登录。"

    def get_captcha(self, driver, wait, id_name, top=0, left=0, width=0):
        try:
            img = wait.until(EC.presence_of_element_located((By.ID, id_name)))
        except common.exceptions.TimeoutException:
            return "请求超时。"
        time.sleep(3)  # 保证图片刷新出来

        captcha = self.get_screenshot(driver, id_name, img.size)

        if left == 0:
            css_style = '{\"' + img.get_attribute('style').replace(' ', '').replace('px', '').replace(';', ', \"') \
                .replace(':', '\": ').strip(', \"') + '}'
            block_json = json.loads(css_style)
            return block_json['top'], block_json['left'], block_json['width']
        else:
            captcha = captcha.crop((left + width, top, img.size['width'], top + width))
            captcha.save('Images/' + id_name + '.png')
            return captcha

    def get_screenshot(self, driver, id_name, adjust_size):
        file_path = 'Images/' + id_name + '.png'
        driver.find_element_by_id(id_name).screenshot(file_path)
        Image.open(file_path).resize((adjust_size['width'], adjust_size['height']), Image.ANTIALIAS).save(file_path)
        return Image.open(file_path)

    def get_distance(self, slideBkg):
        img_rgb = slideBkg.convert('RGB')
        for i in range(0, slideBkg.size[0] - 1, 3):
            R, G, B = img_rgb.getpixel((i, 20))
            if R < 100 and G < 100 and B < 100 and i > slideBkg.size[0] / 2:
                RGB = img_rgb.getpixel((i + 5, 20))
                if RGB[0] < 100 and RGB[1] < 100 and RGB[2] < 100:
                    return i

    def get_tracks(self, distance):
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 1
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance / 2

        while current < distance:
            a = 30 if current < mid else -40
            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            if s < distance - current:
                # 添加到轨迹列表
                tracks.append(round(s))
                # 当前的位置
                current += s
                # 速度已经达到v,该速度作为下次的初速度
                v = v0 + a * t
            else:
                tracks.append(int(distance - current))
                return tracks

    def login(self):
        self.driver.get(self.login_url)
        try:
            return self.click_submit()
        except requests.exceptions.ConnectionError:
            self.driver.close()
            return "网络恍惚！稍后再试！"
