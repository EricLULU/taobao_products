from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib import parse
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import json   #写入json 格式
import time


browser = webdriver.Firefox()
wait = WebDriverWait(browser, 30)

KEYWORD = '手机'
MaxPage = 100   #最大页数
count = 0  #控制变量
sroll_cnt = 0  #下来控制次数
def html_get(page):
    """
        获取html生成
    """
    global sroll_cnt 
    print("正在",page,'页')
    url = "https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA"
    browser.get(url)
    try:
        """
            首先寻找输入框
        """
        input_p = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#spulist-pager .form>input')))
        submit_p = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#spulist-pager .form>.btn')))

        input_p.clear()
        input_p.send_keys(page)
        submit_p.click()
        """
        target = browser.find_element_by_id("#spulist-pager .items .item.active>span")
        browser.execute_script("arguments[0].scrollIntoView();", target) #拖动到可见的元素去
        """
        time.sleep(3)
        #browser.execute_script('window.scrollBy(0, document.body.scrollHeight)')
        while  True:
            if sroll_cnt < 5:
                browser.execute_script('window.scrollBy(0, 1000)')
                time.sleep(0.2)
                sroll_cnt += 1
            else:
                break
        sroll_cnt = 0   #复位

        print("开始等待")
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#spulist-pager .items .item.active>span'), str(page)))
        print("第一个等待已经结束")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#spulist-grid .grid-container #J_SPUBlankRow11 .grid-item .title-row")))
        
        get_product()   #转到获取商品页面
    except TimeoutException:
        print("超时")
        html_get(page)   #超时重新调用



def get_product():  
    """
        获取商品信息
    """
    global count
    html = browser.page_source  #获取商品xinxi
    soup = BeautifulSoup(html,'lxml')
    item_list = soup.select('#spulist-grid .grid-container .grid-item')
    if count < 1:
        with open('taobao.txt','w', encoding='utf-8') as f:
            #data = json.dumps(item_list)
            f.write(html)
            count += 1

    print(len(item_list))
    for item in item_list:
        try:
            product = {
                "name":item.select('.title-row .product-title')[0].attrs['title']
            }
            print(product)
        except:
            pass


    

    """
    print(len(html))
    doc = pq(html)
    item_list = doc('#spulist-grid .grid-item .grid-item')
    for item in item_list:
        product = {
            'image':item.find("img").attr['src']
        }
        print(product)
    """

def main():
    for i in range(1, MaxPage+1):
        html_get(i)

if __name__ == '__main__':
    main()