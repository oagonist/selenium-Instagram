#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 16:56:27 2021

@author: caojiajia
"""
#pip install python-dotenv
#pip install selenium

#爬蟲 #顯性等待
from selenium import webdriver #利用selenium做爬蟲
from selenium.webdriver.common.alert import Alert #處理跳窗
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#隨機抽獎功能
import time
import random

#處理環境變數
import os
from dotenv import load_dotenv
 
def test():
    #----------------前置資料處理
    wanted_comment = "我也要心機彩粧雪花香氛魔法盒" #指定留言內容
    winner_num = 5  #中獎人數
    tag_num = 0  #標記人數
    repeated = False  #可否重複中獎
    total_datas = []
    winning_datas = []
    data = dict()

    post_URL = 'https://www.instagram.com/p/CUhBFquvenp/' #文章網址
 
    driver_path = '/Volumes/珈嘉專用/產業新尖兵/爬蟲小組專題專區/chromedriver'
    browser = webdriver.Chrome(driver_path)
 
    #----------------開始爬蟲 登入
    web = 'https://www.instagram.com/accounts/login/'; #ig登入
    browser.get(web)
 
    ig_account_ele = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
    print(ig_account_ele)
 
    ig_account_ele.send_keys('jason56578@gmail.com')#將使用者的資訊填入
 
    ig_password_ele = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
    print(ig_account_ele)
 
    ig_password_ele.send_keys('2xjialjl')#將使用者的資訊填入
 
 
    login_ele = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
    login_ele.click()
    
    login_ele = WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]')))
    login_ele.click()
    #確認登入狀態
    WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]//*[contains(@class,"_47KiJ")]')))
 
# In[爬蟲 到指定網址進行爬蟲]
    browser.get(post_URL)
 
    post =  WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button')))
    print(post)
    scroll_time = 0
 
    #確定while的停止條件(done)
    #做抽留言條件()
    #做資料處理轉換成json
    maxTop = 0
    stop = False

    while scroll_time<10:
        #滑動
        scrollTop = browser.execute_script('arguments[0].scrollTop +=300;return arguments[0].scrollTop', post)
        scroll_time+=1
        print(scrollTop)
        if scrollTop>950: #每次scroll如果看得到load more就點 
            print("執行中")
            more_ele =  WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button')))
            more_ele.click()
        #終止條件
        if scrollTop>maxTop: #代表有下滑到則將maxtop換為新的然後繼續滑
            maxTop = scrollTop 
        elif scrollTop == maxTop: #代表上次的和這次的一樣已經沒有新留言了
            stop = True
        time.sleep(1)
        scroll_time+=1
    #爬取資料 
    comments = browser.find_elements_by_class_name("Mr508")
    #做資料的處理
    for comment in comments:
        #在此處就要判斷tag人數了
        tag = comment.find_elements_by_class_name("notranslate")
        #print(len(tag))
        if len(tag)>=tag_num:
            comment_data= comment.text.split("\n")
            print(comment_data)
            #判斷使用者要的留言內容
            #判斷tag人數
            if wanted_comment in comment_data[1]:
                data["user_id"] = comment_data[0]
                data["comment"] = comment_data[1]
                
                total_datas.append(data)
                #清空重來
                data={}
            comment_data={}
    print(total_datas)
    if len(total_datas) <winner_num:
        print("留言人數太少")
    else:
        #抽獎迴圈
        num = 0
        while num < winner_num:
            repeatOrNot = False #看看當前是否重複
            winner = random.randint(0,len(total_datas)-1)  
            print(num)
            #做重複留言邏輯
            if repeated == False:
                #確認此data是否有重複 若重複則num-1 讓迴圈多跑一次
                for data in winning_datas:
                    if total_datas[winner]["user_id"] in data['user_id']:
                        print("重複")
                        num-=1
                        repeatOrNot = True
                #如果不重複則一樣append dtat
                if repeatOrNot == False:
                    winning_datas.append(total_datas[winner])
            else: #直接選出
                winning_datas.append(total_datas[winner]) 
            num+=1
        print(winning_datas)
         
       
test()
