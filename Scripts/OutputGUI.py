from tkinter import *
from Scripts.DBHelper import DBHelper

class OutputGUI:

    def __init__(self, keywords, window, scroll_text):
        self.window = window
        self.scrolled_text = scroll_text
        self.title_label = Label(self.window, text="查询结果：", anchor='w')
        self.title_label.place(x=20, y=30, width=100, height=20)
        self.title_label.configure(bg="#f8f8f8")
        self.hint_label = Label(self.window, text="视情况已为您推荐下列书籍，相关评价请滚动文本框查看。", anchor='w')
        self.hint_label.place(x=20, y=50, width=360, height=20)
        self.hint_label.configure(bg="#f8f8f8")
        self.table_name = str(keywords).replace(" ", "_").replace("+", "_")
        self.helper = DBHelper()
        self.show_book_details()

    def show_book_details(self):
        book_detail_list = self.helper.show_book_detail(self.table_name + "_info")
        index = 1
        for item in book_detail_list:
            self.scrolled_text.insert(INSERT, "No." + str(index) + " 《" + item[1] + "》\n")
            self.scrolled_text.insert(INSERT, "评分: " + str(item[2]) + "\n")
            self.scrolled_text.insert(INSERT, "ISBN: " + str(item[3]) + "\n")

            public_comment_list = self.helper.show_book_comment(self.table_name + "_public", str(item[0]))
            if public_comment_list.__len__() != 0:
                self.scrolled_text.insert(INSERT, "------------------------------------------------\n")
                self.scrolled_text.insert(INSERT, "[大众评价]\n")
                for comment_detail in public_comment_list:
                    self.scrolled_text.insert(INSERT, comment_detail[0] + ": " + comment_detail[1] + "\n")

            friend_comment_list = self.helper.show_book_comment(self.table_name + "_friends", str(item[0]))
            if friend_comment_list.__len__() != 0:
                self.scrolled_text.insert(INSERT, "------------------------------------------------\n")
                self.scrolled_text.insert(INSERT, "[友邻评价]\n")
                for comment_detail in friend_comment_list:
                    self.scrolled_text.insert(INSERT, comment_detail[0] + ": " + comment_detail[1] + "\n")
            index += 1
            self.scrolled_text.insert(INSERT, "================================================\n")
        self.window.update_idletasks()
        self.helper.close_connection()


