import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import threading
import requests
from bs4 import BeautifulSoup
import util_config
import os
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import GUI
from tkinter import simpledialog

iscontinue=True
canvas=None
myframes=None

#保存图片
def save_image_from_url(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join('./image', filename)
        os.makedirs('./image', exist_ok=True)  # 创建文件夹
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print("图片保存成功！")
    else:
        print("无法下载图片。")


#打开浏览器
def openChrome():
    cmd = '"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="C:\selenium\ChromeProfile"'
    subprocess.run(cmd)


#处理HTML
def handleHTML(html_doc):
    global iscontinue
    global canvas
    global myframes
    # 使用BeautifulSoup解析HTML
    htmltext = html_doc.get_attribute('outerHTML')
    soup = BeautifulSoup(htmltext, 'lxml')
    Products = soup.find_all('tr', class_='boo-table-row')
    y=0
    for item in Products:
        if iscontinue:
            return
        pro={}
        title = item.find_all('div', class_='edit-input')
        print(title[0]['value'])
        image = item.find_all('img')[0]['data-src']
        print(image)
        titletext=title[0]['value']
        for char in ['\\', '/', '<', '>', ':', '"', '|', '?', '*']:
            titletext = titletext.replace(char, '-')
        print(titletext)
        #保存图片
        save_image_from_url(image,titletext+".jpg")

        sum = 0
        products = util_config.get("products")
        isitem = True
        for iem in products:
            if iem["title"] == title[0]['value']:
                iem["image"] = titletext + ".jpg"
                iem["title"] = title[0]['value']
                iem["price"] = item.find_all('span', class_='number')[0].get_text(strip=True)
                iem["stock"] = item.find_all('span', class_='number')[1].get_text(strip=True)
                print(iem)
                util_config.update_list("products", sum, iem)
                isitem = False
            sum += 1

        pro["image"]=titletext+".jpg"
        pro["title"]=title[0]['value']
        pro["price"]=item.find_all('span', class_='number')[0].get_text(strip=True)
        pro["stock"] = item.find_all('span', class_='number')[1].get_text(strip=True)
        print(pro)
        #添加到json文件

        if isitem:
            util_config.append_list("products",pro)
        time.sleep(1)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def on_button_click(title,Cost_label):
            new_Cost = simpledialog.askstring("成本价", f"请{title}输入新的成本价:")
            if new_Cost:
                Cost_label.config(text="成本价：" + new_Cost)
                print(f"{title}新的成本价: {new_Cost}")
                products = util_config.get("products")
                sum = 0
                for item in products:
                    if item["title"] == title:
                        item["Cost"]=new_Cost
                        print(item)
                        util_config.update_list("products",sum,item)
                    sum+=1

        #容器
        myframes.bind("<MouseWheel>", on_mousewheel)
        frame = Frame(myframes)
        #frame.place(x=0, y=y, width=500, height=90)
        frame.pack(anchor='w')
        frame.bind("<MouseWheel>", on_mousewheel)

        # 添加图片
        image_path = "./image/"+pro["image"]
        img = Image.open(image_path)
        img = img.resize((70, 70))  # 调整图片大小
        img_tk = ImageTk.PhotoImage(img)
        image_label = Label(frame, image=img_tk)
        image_label.image = img_tk  # 保持对图像的引用，以防止被垃圾回收
        #image_label.place(x=20, y=10)  # 设置图片的位置
        image_label.pack(side=LEFT, padx=10)
        image_label.bind("<MouseWheel>", on_mousewheel)

        # 添加标签
        text = pro["title"]
        text_label = Label(frame, text=text)
        #text_label.place(x=100, y=10, width=378, height=30)
        text_label.pack(side=TOP)
        text_label.bind("<MouseWheel>", on_mousewheel)

        price_label = Label(frame, text="价格："+pro["price"], anchor="center", )
        #price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=LEFT, padx=10,anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        stock_label = Label(frame, text="库存："+pro["stock"], anchor="center", )
        #stock_label.place(x=200, y=50, width=100, height=30)
        stock_label.pack(side=LEFT,anchor='w')
        stock_label.bind("<MouseWheel>", on_mousewheel)

        if item.get("Cost"):
            Cost_label = Label(frame, text="成本价：" + pro["Cost"], anchor="center", )
            # stock_label.place(x=200, y=50, width=100, height=30)
            Cost_label.pack(side=LEFT, anchor='w')
            Cost_label.bind("<MouseWheel>", on_mousewheel)

            btn = Button(frame, text="修改成本价", takefocus=False, )
            btn.pack(side=LEFT, anchor='w')
            btn.bind("<Button-1>", lambda event, title=pro["title"], Cost_label=Cost_label: on_button_click(title,Cost_label))
            btn.bind("<MouseWheel>", on_mousewheel)
        else:
            Cost_label = Label(frame, text="成本价：", anchor="center", )
            # stock_label.place(x=200, y=50, width=100, height=30)
            Cost_label.pack(side=LEFT, anchor='w')
            Cost_label.bind("<MouseWheel>", on_mousewheel)

            btn = Button(frame, text="添加成本价", takefocus=False, )
            btn.pack(side=LEFT, anchor='w')
            btn.bind("<Button-1>",lambda event, title=pro["title"], Cost_label=Cost_label: on_button_click(title, Cost_label))
            btn.bind("<MouseWheel>", on_mousewheel)


        y+=95
        #frames.update()
        # 更新 Canvas 的滚动区域
        #canvas.create_window((0, 0), window=myframes, anchor="nw")
        GUI.updateframe(myframes,canvas)
        # myframes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # canvas.config(scrollregion=canvas.bbox("all"))


#主程序（控制浏览器，获取元素）
def jiankong():
    global urllist
    global iscontinue
    caps = {
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY',
        'goog:loggingPrefs': {'performance': 'ALL'},  # 记录性能日志
        'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}  # 无界面模式
    }
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    browser = webdriver.Chrome(executable_path=r".\chromedriver-win64\chromedriver.exe", options=options,desired_capabilities=caps)
    browser.get("https://shangoue.meituan.com/#/reuse/sc/product/views/product/list")
    browser.minimize_window()
    time.sleep(3)
    current_url = browser.current_url
    print(current_url)
    if current_url == "https://waimaie.meituan.com/new_fe/login_gw#/login":
        try:
            element = browser.find_element(by=By.XPATH, value="//input[@id='login']")
            element.send_keys("wmcxyc623917")
            element = browser.find_element(by=By.XPATH, value="//input[@id='password']")
            element.send_keys("BeiTai2023")
            time.sleep(1)
            element = browser.find_element(by=By.XPATH, value="//div[@class='ep-checkbox-container']")
            element.click()
        except Exception as e:
            print("没有该元素！：", e)
            pass
    try:
        mask = browser.find_element(By.XPATH, "//div[@class='boo-modal-mask']")
        browser.execute_script("arguments[0].style.display= 'none';", mask)
        wrap = browser.find_element(By.XPATH, "//div[@class='boo-modal-wrap']")
        browser.execute_script("arguments[0].classList.add('boo-modal-hidden')", wrap)
        # actions = ActionChains(browser)
        # # 在空白区域上模拟鼠标点击
        # actions.click(popup)
    except Exception as e:
        print("没有遮挡元素！")
        pass
    time.sleep(3)
    iframe_element = browser.find_element(by=By.XPATH, value="//iframe[@id='hashframe']")
    browser.switch_to.frame(iframe_element)

    Productslist = browser.find_element(by=By.XPATH, value="//div[@class='table-with-page']")
    Products = Productslist.find_element(by=By.XPATH, value="//tbody[@class='boo-table-tbody']")
    time.sleep(1)
    ul = Products.find_element(by=By.XPATH, value="//ul[@class='boo-page table-with-page-page']")
    li = ul.find_elements(by=By.XPATH, value="//li[@class='boo-page-item']")
    sum=1
    for i in li:
        sum = int(i.text) if int(i.text) > sum else sum
    print("共",sum,"页")
    for i in range(0,sum):
        if iscontinue:
            print("结束线程！")
            browser.close()
            return
        print('第',i+1,'页')
        time.sleep(3)
        Productslist = browser.find_element(by=By.XPATH, value="//div[@class='table-with-page']")
        Products = Productslist.find_element(by=By.XPATH, value="//tbody[@class='boo-table-tbody']")
        handleHTML(Products)
        time.sleep(1)
        ul = Products.find_element(by=By.XPATH, value="//ul[@class='boo-page table-with-page-page']")
        li = ul.find_element(by=By.XPATH, value="//li[@title='下一页']")
        li.click()
    browser.close()
    print("爬取完毕！")
    return
    # if len(menu_items) > 1:
    #     # 触发第二个元素的点击事件
    #     menu_items[1].click()
    #     print("订单管理！")
    # else:
    #     print("没有找到第二个class为'roo-plus-menu-sub'的li元素")
    # # menu_items.click()
    # time.sleep(3)
    # iframe_element = browser.find_element(by=By.XPATH, value="//iframe[@id='hashframe']")
    # browser.switch_to.frame(iframe_element)
    # OrderList = browser.find_elements(by=By.XPATH, value="//div[@class='order-card-container divide-line']")
    # print("订单详情！")
    # # print(OrderList)
    # processOrders(OrderList)

#主函数，多线程
def main(myframe,my_canvas):
    global iscontinue
    global canvas
    global myframes
    iscontinue = False
    canvas = my_canvas
    myframes = myframe
    #json_file_path = "./config.json"
    # if os.path.exists(json_file_path):
    #     os.remove(json_file_path)
    #     print("JSON文件删除成功！")
    # else:
    #     print("JSON文件不存在！")
    # image_folder_path = "./image"
    # if os.path.exists(image_folder_path):
    #     for file_name in os.listdir(image_folder_path):
    #         if file_name.endswith(".jpg") or file_name.endswith(".png"):
    #             file_path = os.path.join(image_folder_path, file_name)
    #             os.remove(file_path)
    #     print("所有图片文件删除成功！")
    # else:
    #     print("图片文件夹不存在！")
    util_config.init_conf()
    thread = threading.Thread(target=openChrome)
    thread2 = threading.Thread(target=jiankong)
    thread.start()
    thread2.start()


#入口
if __name__ == "__main__":
    main()
