Table of Contents
=================
* [简易豆瓣书籍推荐器](#简易豆瓣书籍推荐器)
     * [效果演示图](#效果演示图)
  * [项目介绍](#项目介绍)
  * [项目背景](#项目背景)
  * [推荐机制](#推荐机制)
  * [如何运行本项目](#如何运行本项目)
  * [小结](#小结)
 
# 简易豆瓣书籍推荐器
[![LICENSE](https://img.shields.io/cocoapods/l/AFNetworking.svg)](https://github.com/Hephaest/DoubanCrawler/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/release/python-380/)
[![Dependencies](https://img.shields.io/badge/Dependencies-up%20to%20date-green.svg)](https://github.com/Hephaest/DoubanCrawler/tree/master/Scripts)

**中文 (Only in Chinese)**

最后一次更新于 `2020/4/5`

### 效果演示图

<p align="center"><img src ="Images/ui.gif" width = "600px"></p>

## 项目介绍
这是一个豆瓣小爬虫，用于推荐给豆瓣用户 TA 可能喜欢的**有方向性的**书籍。豆瓣书籍的搜索方式很奇怪:<br>
- 首先，书籍并不是按照评分排序的，用户嫌麻烦并不会往后翻很多次，这导致有些高分书籍会被用户忽略。
- 其次，大众喜欢的书籍并不一定是用户认为的"好/有品位"的书，但是用户的阅读偏好可以通过其友邻的评分进行猜测。

## 项目背景
学习是不断探索的过程，不应该止于讲师推荐的`厚重的外文教材`或`过时又喜欢装深沉搞文字游戏的中文教材`，本项目主要就是提供这个用途的 - **推荐值得看的专业领域的书籍**。

因为上面提到的豆瓣搜索的问题，我之前一直对找"课本"这件事情非常头疼。再强调一下，高分书籍不一定是写得好(简单易懂/有品味)的书，所以大家一定要找合适自己的书。如何找合适自己的书呢？请先从关注和自己研究方向相同水平较高且品味较一致的豆友开始吧~

## 推荐机制
1. 海量筛选，根据关键词先把相关联的书籍全部找出来。
2. 把大众评分大于 7 的书籍都挑出来(低于 7 的基本可以认为不值得一读了)
3. 查看所有第 2 步挑出来的书的还有评分，总评加权`6 : 4`，**6 成看友邻的评分**，只有友邻找得好，你最终得到的评分就越真实。
4. 根据总评选出前 10 本书，一开始学习的时候 10 本专业书籍就足够 cover 整个知识体系了，一般用户也不会一次读 10 本的。

## 如何运行本项目
要成功运行本项目有三个先决条件:
1. PC 上安装了 Python 的 IDE(Pycharm 最佳)，且支持 Python 3.0+ 的版本
2. 下载并安装了 chromedriver，安装地址请点击此[链接](https://chromedriver.chromium.org/downloads)
3. 安装了以下 packages，用于下图中的破解图片识别和爬虫:
    - selenium
    - Pillow
    - requests

<p align="center"><img src ="Images/login.gif" width = "600px"></p>

满足这三条要求的同学就可以直接通过命令行或者 Pycharm 的 **Run** 运行了哦！<br>
为了简化登录输入操作，同学们可以先提前把账号密码写入 Account 文件夹下的 txt 里。格式 `username password`。<br>
一杯☕️的时间，专属你的推荐书单就生成完毕了～

## 小结
- 这是去年暑假写的小爬虫，但是后来生活发生了变化就一直没有整理出来...
- 本爬虫仅供学习交流使用，目的是帮助豆瓣用户更好的获取(有用的)站内资源。
- 如果大家有什么想提的问题，欢迎在 issue 向我提问，有更好的实现请 pull request! 
