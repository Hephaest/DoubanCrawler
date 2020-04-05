import time
from tkinter import *
from selenium import common
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Scripts.DBHelper import DBHelper


def find_author(a_link):
    return a_link.text


class BookSpider:
    def __init__(self, driver, wait, window, progress_bar, style, scroll_text):
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.label_name = ''
        self.driver = driver
        self.wait = wait
        self.helper = DBHelper()
        self.window = window
        self.progress_bar = progress_bar
        self.style = style
        self.scrolled_text = scroll_text

    def find_book_by_name(self, name):
        while name is None:
            time.sleep(1)

        start = 0
        stop = False

        self.label_name = str(name).replace(" ", "_").replace("+", "_")
        self.helper.drop_table(self.label_name + "_friends")
        self.helper.drop_table(self.label_name + "_public")
        self.helper.drop_table(self.label_name + "_info")
        self.helper.drop_table(self.label_name)
        self.helper.create_table(self.label_name)
        self.driver.get("https://book.douban.com/subject_search?search_text=" + name + "&cat=1001&start=0")

        try:
            while stop is False:
                request_url = "https://book.douban.com/subject_search?search_text=" + name + "&cat=1001&start=" + str(
                    start)

                self.driver.get(request_url)
                time.sleep(3)
                book_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="item-root"]')))
                for book in book_list:
                    try:
                        book_rating = book.find_element_by_xpath('.//span[@class="rating_nums"]').text
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue

                    book_id = re.search(r'[0-9]+',
                                        book.find_element_by_xpath(".//a[@class=\"title-text\"]").get_attribute("href"),
                                        re.M | re.I).group()
                    self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 查看 subject id: " + book_id + "\n")
                    self.window.update_idletasks()
                    self.helper.add_uid_and_rating(self.label_name, "uid", "rating", book_id, book_rating)
                start += 15
                self.helper.submit_commit()
                try:
                    self.driver.find_element_by_xpath('.//a[@class="next"]')
                except common.exceptions.NoSuchElementException:
                    stop = True

            try:
                self.progress_bar['value'] = 40
                self.style.configure("green.Horizontal.TProgressbar", text="40%")
                self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + "初步筛选完成!\n")
                self.window.update_idletasks()
                self.helper.find_ratings_above_7(self.label_name)
                self.find_book_detail()
                return 0
            except:
                return -1

        except common.exceptions.TimeoutException:
            self.progress_bar['value'] = 40
            self.style.configure("green.Horizontal.TProgressbar", text="40%")
            self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + "服务异常，请稍后再试 (1006)\n")
            self.window.update_idletasks()
            self.driver.close()

    def find_book_detail(self):
        uid_list = self.helper.find_uid(self.label_name + "_info")
        for uid in uid_list:
            subject_id = str(uid[0])
            self.driver.get("https://book.douban.com/subject/" + subject_id + "/")
            time.sleep(3)
            book_intro = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="wrapper"]//div[@id="content"]')))
            self.driver.execute_script("window.stop();")

            book_title = DBHelper.replace_escape_symbols(book_intro.find_element_by_xpath('.//preceding-sibling::h1//span').text)
            self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 获取《" + book_title + "》相关的信息\n")
            self.window.update_idletasks()

            try:
                author = book_intro.find_element_by_xpath('.//div[@id="info"]/br[1]/preceding-sibling::a').text
            except common.exceptions.NoSuchElementException:
                author_list = book_intro.find_elements_by_xpath('.//div[@id="info"]//span[1]/a')
                author = '/'.join([find_author(author) for author in author_list])
            author = DBHelper.replace_escape_symbols(author)

            inner_html = book_intro.find_element_by_xpath('.//div[@id="info"]').get_attribute("innerHTML")

            try:
                publisher = re.search(r'出版社:</span>(.*)<br>', inner_html, re.M | re.I).group(1)
            except AttributeError:
                publisher = "NULL"
            publisher = DBHelper.replace_escape_symbols(publisher)

            publish_date = re.search(r'(\s\d{4})-(\d{1,2})-(\d{1,2})|(\s\d{4})-(\d{1,2})|(\s\d{4})', inner_html, re.M | re.I).group()
            ISBN = re.search(r'(\d{10,13})', inner_html, re.M | re.I).group()

            p_rating = float(self.helper.find_rating(self.label_name + "_info", subject_id)[0][0])

            f_rating = "NULL"
            final_rating = 0.0
            try:
                f_rating = book_intro.find_element_by_class_name('rating_avg').text
                final_rating = float(f_rating) * 0.6 + p_rating * 0.4
            except common.exceptions.NoSuchElementException:
                f_rating = "NULL"
                final_rating = p_rating
            finally:
                self.helper.update_book_detail(self.label_name, subject_id, f_rating, book_title, author,
                                               publisher.strip(' '), publish_date.strip(' '), ISBN, str(final_rating))

        self.helper.submit_commit()
        self.progress_bar['value'] = 60
        self.style.configure("green.Horizontal.TProgressbar", text="60%")
        self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + "评分计算结束!\n")
        self.window.update_idletasks()

        self.find_public_comment()
        self.progress_bar['value'] = 80
        self.style.configure("green.Horizontal.TProgressbar", text="80%")
        self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + "成功捕获热门评分!\n")
        self.window.update_idletasks()

        self.find_friend_comment()
        self.progress_bar['value'] = 100
        self.style.configure("green.Horizontal.TProgressbar", text="100%")
        self.scrolled_text.insert(INSERT, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + "成功捕获豆友评分!\n")
        self.window.update_idletasks()

        # time.sleep(200)
        # self.driver.close()

    def find_public_comment(self):
        self.helper.create_public_comment(self.label_name)
        uid_list = self.helper.find_rating_top_10(self.label_name + "_info")
        for uid in uid_list:
            subject_id = str(uid[0])
            self.driver.get("https://book.douban.com/subject/" + subject_id + "/")
            time.sleep(3)
            comment_root = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="comment-list hot show"]')))
            self.driver.execute_script("window.stop();")
            user_list = comment_root.find_elements_by_xpath('.//div[@class="comment"]')
            for user in user_list:
                self.helper.add_comment(self.label_name + "_public", "uid", "name", "comment", subject_id,
                                        DBHelper.replace_escape_symbols(user.find_element_by_xpath('.//span[@class="comment-info"]//a').text),
                                        DBHelper.replace_escape_symbols(user.find_element_by_xpath('.//span[@class="short"]').text))
        self.helper.submit_commit()

    def find_friend_comment(self):
        self.helper.create_friend_comment(self.label_name)
        uid_list = self.helper.find_rating_top_10(self.label_name + "_info")
        for uid in uid_list:
            subject_id = str(uid[0])
            self.driver.get("https://book.douban.com/subject/" + subject_id + "/comments/follows")
            time.sleep(3)
            comment_root = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'comments-wrapper')))
            self.driver.execute_script("window.stop();")
            comments = comment_root.find_element_by_xpath('.//span[@id="total-comments"]').text
            number = re.search(r'(\d+)', comments, re.M | re.I).group()
            if number == 0:
                continue

            user_list = comment_root.find_elements_by_xpath('.//div[@class="comment"]')
            for user in user_list:
                self.helper.add_comment(self.label_name + "_friends", "uid", "name", "comment", subject_id,
                                        DBHelper.replace_escape_symbols(user.find_element_by_xpath('.//span[@class="comment-info"]//a').text),
                                        DBHelper.replace_escape_symbols(user.find_element_by_xpath('.//span[@class="short"]').text))
                self.helper.submit_commit()
        self.helper.close_connection()