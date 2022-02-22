from tkinter.tix import Tree
from turtle import pos
from xmlrpc.client import FastParser
from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint, random
from random import shuffle

chrome_browser = webdriver.Chrome()
chrome_browser.maximize_window()
posts = []
accs = []
tags =[]
linkbyTag = ""


# def decorator(func):
#     def wrapper(*arg, **kwargs):
#         func(*arg, **kwargs)
#         time.sleep(2)
#         controller()
#     return wrapper


# @decorator
def login(username , password):
    """
    logs into your account .
    needs username and password to be passed 
    """
    chrome_browser.get("https://www.instagram.com/")
    try:
        exist = WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
        # print(allCards)    
    except:
        print("exist")
    finally:
        inputs = chrome_browser.find_elements_by_tag_name("input")
        inputs[0].send_keys(username)
        inputs[1].send_keys(password)
        time.sleep(2)
        btn = chrome_browser.find_element_by_css_selector("button > div")
        print(btn)
        btn.click()
        time.sleep(4)


def unfollow(username):
    chrome_browser.get(f"https://www.instagram.com/{username}/following/")
    try :
            divlist = WebDriverWait(chrome_browser , 10).until(EC.presence_of_element_located((By.CLASS_NAME , "jSC57")))
    except:
            print("error 0{divlist}")
    followingList = chrome_browser.find_element_by_css_selector("ul.jSC57").find_element_by_tag_name("li")
    unfollowBtn = []
    for f in followingList:
        unfollowBtn.append(f.find_element_by_tag_name("button"))
    for btn in unfollowBtn:
        btn.click()
        try :
            div = WebDriverWait(chrome_browser , 10).until(EC.presence_of_element_located((By.CLASS_NAME , "mt3GC")))
        except:
            print("error")
        if div:
            sub= chrome_browser.find_element_by_class_name("-Cab_")
            sub.click()
# @decorator
def setTag(tagname):
    """
    set a tag name to find posts with.
    """
    print(tagname)
    global linkbyTag 
    if tagname =="":   
        tagname = input("please enter your tag : \n\t")
    if len(tagname) > 20 :
        linkbyTag = tagname
    else:
         linkbyTag = f"https://www.instagram.com/explore/tags/{tagname}"


# @decorator
def getPosts():
    """
    finds posts with tag name
    """
    global linkbyTag
    global posts
    countForThisTag =0 
    try:
        chrome_browser.get(linkbyTag)
        time.sleep(5)
        allLinks = chrome_browser.find_elements_by_css_selector("a")
        
        for link in allLinks:
            if countForThisTag < 25:
                temp = re.template(r"(?=\/p\/)")
                href = link.get_attribute("href")
                res = temp.findall(href)
                if res and randint(0,10)>2:
                    posts.append(href)
                    countForThisTag += 1
            else:
                print("max size reached !!")
                break
    except Exception as err:
        print(f"error in getting posts : {err}")
    time.sleep(5)
    
# @decorator
def likePosts():
    """likes a list of posts . you need to define posts first in getPosts()"""
    index = 0
    print(f"total is : {len(posts)}")
    shuffle(posts)
    for p in posts:
        chrome_browser.get(p)
        try:
          likebut = WebDriverWait(chrome_browser, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "ltpMr"))
            )  
        except Exception as err:
            print(f"something went wrong !! : \n\t{err}")
            continue
        if likebut :
            parel= chrome_browser.find_element_by_css_selector(".ltpMr ")
            isLiked = parel.find_element_by_css_selector("._8-yf5 ")
            isLiked = isLiked.get_attribute("fill")  
            print(isLiked)
            if isLiked == "#262626":
                all_actions = chrome_browser.find_elements_by_css_selector("section.ltpMr > span")
                all_actions[0].click()
                index += 1
                time.sleep(4)
                print(f"* index is: {index} *")
            else: 
                print("already liked !")

# @decorator
def cmAndLike(cmlist):
    """gets a list of comments to post under any video or pic(randomly)"""
    shuffle(posts)
    totalCommented = 0
    index = 0
    for p in posts : 
        # time.sleep(5)
        if totalCommented > 70:
            print("max comment reached !!")
            break
        try:
          chrome_browser.get(p)
          time.sleep(4)
          likebut = WebDriverWait(chrome_browser, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "ltpMr"))
            )  
        except Exception as err:
            print(f"something went wrong !! : \n\t{err}")
            continue
        if likebut :
            parel= chrome_browser.find_element_by_css_selector(".ltpMr ")
            isLiked = parel.find_elements_by_css_selector("._8-yf5 ")
            isLiked = isLiked[1].get_attribute("fill")  
            print(isLiked)
            if isLiked == "#262626":
                all_actions = chrome_browser.find_elements_by_css_selector("section.ltpMr > span")
                all_actions[0].click()
                index += 1
                time.sleep(5)
                print(f"* index is: {index} *")
            else: 
                print("already liked !")
                continue
        try:
          element = WebDriverWait(chrome_browser, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "Ypffh"))
            )
        except Exception as err:
            print(f"something went wrong !! : \n\t{err}")
            continue
        if element :
            try:
                if randint(0,10) > 3 :
                    textarea = chrome_browser.find_element_by_class_name("Ypffh")
                    form = chrome_browser.find_element_by_class_name("X7cDz")
                    textarea.click()
                    textarea = chrome_browser.find_element_by_class_name("Ypffh")
                    cm = cmlist[randint(0 , len(cmlist)-1)]
                    textarea.send_keys(cm)
                    form.submit()
                    totalCommented+=1
                    time.sleep(5)
            except Exception as err:
                print(f"something went wrong !! : \n\t{err}")
                print(f"checkout comment : {cm} .")
                continue

# @decorator   
def findSimilar(keyword):
    """
    finds any similar account or tag,similar to your keyword. 
    pass the keyword to set the list of accounts 
    """
    try:
        searcher = WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "XTCLo"))
            )    
    except:
        print("searcher")
    search = chrome_browser.find_element_by_class_name("XTCLo")
    search.clear()
    search.send_keys(keyword)
    time.sleep(5)
    try:
        allCards = WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fuqBx"))
            )
        # print(allCards)    
    except:
        print("allCards")
    if allCards :
        allLinks = chrome_browser.find_elements_by_class_name("-qQT3")
        for link in allLinks:
            if len(accs) > 55:
                print("max size reached !!")
                break
            l = link.get_attribute("href")
            isTag = l.find("tags") 
            if isTag== -1:
                accs.append(l)
            else:
                tags.append(l)

    print(f"{len(tags)} tags are detected")
    print(f"{len(accs)} accounts are detected")
    
# @decorator
def follow():
    """
    follows users by account username . 
    first use findSimilar() to set the account list
    """
    totalFollowed = 0
    print(accs)
    while totalFollowed <50:
        shuffle(accs)
        for acc in accs:
            chrome_browser.implicitly_wait(2)
            try:
                chrome_browser.get(acc)
                try:
                    followbut = WebDriverWait(chrome_browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_6VtSN"))
                        )
                    # print(allCards)    
                except:
                    print(followbut) 
                if followbut:
                    btn = chrome_browser.find_element_by_class_name("_6VtSN")
                    txt = btn.get_attribute("innerHTML")
                    if txt == "Follow" and worthFollow():
                        chrome_browser.implicitly_wait(4)
                        print( acc[26:len(acc)-1])
                        btn.click()
                        totalFollowed+=1
                        
                else:
                    continue
            except Exception as err :
                print(f"couldnt follow user ! : {err}")
                continue
    print(f"total accs followed : {totalFollowed}")

def worthFollow():
    postNum = chrome_browser.find_element_by_css_selector("span.g47SY")[0].get_attribute("innerHTML")
    if int(postNum) < 2 :
        return False
    followStates = chrome_browser.find_elements_by_css_selector("a.-nal3>span")
    followers = followStates[0].get_attribute("innerHTML")
    followings = followStates[1].get_attribute("innerHTML")
    if int(followers) < 2000 and int(followers) > 50:
        if int(followings) > 50 and int(followings) < 7000:
            user_posts = chrome_browser.find_elements_by_css_selector("div.v1Nh3.kIKUG._bz0w>a")[:2]
            for p in user_posts:
                posts.append(p.get_attribute("href"))
            return True
    return False


def comment(cmlist):
    shuffle(posts)
    totalCommented = 0
    for p in posts : 
        chrome_browser.get(p)
        time.sleep(4)
        # time.sleep(5)
        if totalCommented > 60:
            print("max comment reached !!")
            break
        try:
          element = WebDriverWait(chrome_browser, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "Ypffh"))
            )
        except Exception as err:
            print(f"something went wrong !! : \n\t{err}")
            continue
        if element :
            try:
                textarea = chrome_browser.find_element_by_class_name("Ypffh")
                form = chrome_browser.find_element_by_class_name("X7cDz")
                textarea.click()
                textarea = chrome_browser.find_element_by_class_name("Ypffh")
                cm = cmlist[randint(0 , len(cmlist)-1)]
                textarea.send_keys(cm)
                form.submit()
                totalCommented+=1
                time.sleep(5)
            except Exception as err:
                print(f"something went wrong !! : \n\t{err}")
                print(f"checkout comment : {cm} .")
                continue 

# def controller():
#     print("enter a number from list bellow:\n 0)login\n 1)setting tag name\n 2)get posts\n 3)like all \n 4)comment all \n 5)find \n 6)follow")
#     task = input(":")
#     if task == "0":
#         login()
#     elif task == "1":
#         setTag()
#     elif task == "2":
#         getPosts()
#     elif task == "3":
#         likePosts()
#     elif task == "4":
#         commentPosts()
#     elif task == "5":
#         findSimilar(input("enter the keyword to search : "))
#     elif task == "6":
#         follow()
#     else:
#         print("\nnot Correct !! \n")
#         controller()


# controller()
