from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from tkinter import *
import time
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
from Scripts.BookSpider import BookSpider
from Scripts.LoginCracker import LoginCracker
from Scripts.OutputGUI import OutputGUI
import _thread
import platform


class DoubanSpider:

    def __init__(self, username, password, keywords, tk_window):
        self.username = username
        self.password = password
        self.keywords = keywords
        self.window = tk_window
        self.window.configure(bg="#f8f8f8")
        self.title_label = Label(self.window, text="进度：")
        self.title_label.place(x=20, y=50, width=60, height=20)
        self.title_label.configure(bg="#f8f8f8")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.layout("green.Horizontal.TProgressbar",
                          [("Horizontal.Progressbar.trough",
                            {"children": [("Horizontal.Progressbar.pbar",
                                           {"side": "left", "sticky": "ns"})],
                             "sticky": "nswe"}),
                           ("Horizontal.Progressbar.label", {"sticky": ""})])
        self.style.configure("green.Horizontal.TProgressbar", troughcolor="white", bordercolor="white",
                             background="#61c636", thickness=20)
        self.style.configure("green.Horizontal.TProgressbar", text="0%")
        self.progressBar = ttk.Progressbar(self.window, style="green.Horizontal.TProgressbar", orient=HORIZONTAL,
                                           length=300, mode="determinate")
        self.progressBar.place(x=80, y=50, width=300, height=20)
        self.scrolled_text = tkst.ScrolledText(master=self.window, wrap=WORD, width=100, height=20)
        self.scrolled_text.place(x=20, y=80, width=360, height=270)

        chrome_drive = r"/Users/hephaest/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_drive)
        self.wait = WebDriverWait(self.driver, 60, 10)
        _thread.start_new_thread(self.call_login_cracker, ())

    def call_login_cracker(self):
        login_status = LoginCracker(self.username, self.password, self.driver, self.wait, self.progressBar,
                                    self.style).login()
        self.scrolled_text.insert(INSERT,
                                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + login_status + "\n")
        self.window.update_idletasks()
        search_status = BookSpider(self.driver, self.wait, self.window, self.progressBar, self.style,
                                   self.scrolled_text).find_book_by_name(self.keywords)
        if search_status == 0:
            if platform.system() == "Darwin":
                self.next_btn = Button(self.window, text="查看结果", highlightbackground="#61c636", fg="white",
                                       highlightthickness=30, font=("Arial", 16), command=self.on_click)
            else:
                self.next_btn = Button(self.window, text="查看结果", bg="#61c636", fg="white", font=("Arial", 16),
                                       command=self.on_click)
            self.next_btn.place(x=300, y=360, width=80, height=30)

    def on_click(self):
        self.title_label.destroy()
        self.progressBar.destroy()
        self.scrolled_text.delete("1.0", END)
        self.next_btn.destroy()
        OutputGUI(self.keywords, self.window, self.scrolled_text)
