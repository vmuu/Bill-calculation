import subprocess
# from selenium.webdriver.chrome.options import Options
# from seleniumwire  import webdriver
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import threading
import base64
from PIL import Image
from io import BytesIO
import shutil
import json
from selenium.common.exceptions import WebDriverException, NoSuchElementException, InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import *
from tkinter.ttk import *
import handleHTML
from PIL import ImageTk, Image
import GUI
import util_config
import re
from tkinter import simpledialog

iscontinue=True
myframe=None
mycanvas=None
browser=None
order_info=[]
Cost_labellist= {}
CumulativeProfitlabel=None
CumulativeCostlabel=None

def openChrome():
    cmd = '"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="C:\selenium\ChromeProfile"'
    subprocess.run(cmd)


def processOrders(OrderList):
    global myframe
    global mycanvas
    global browser
    global order_info
    global Cost_labellist
    global CumulativeCostlabel
    global CumulativeProfitlabel
    for item in OrderList:
        order_html = item.get_attribute('outerHTML')
        orderInfo = handleHTML.handleHTML(order_html)
        order_info.append(orderInfo)
        # print(item.text)
        # print()
        # print()
        # print()
        print("订单编号", orderInfo['订单编号'])
        print("顾客姓名", orderInfo['顾客姓名'])
        print("顾客电话", orderInfo['顾客电话'])
        print("商品", orderInfo['商品'])
        print("本单预计收入", orderInfo['本单预计收入'])
        print("本单顾客实际支付（已支付）", orderInfo['本单顾客实际支付（已支付）'])
        # for order in orderInfo['商品']:
        #     product = order['name']
        #     percentage = 70
        #
        #     # 计算要截取的字符数
        #     char_count = int(len(product) * (percentage / 100))
        #
        #     # 使用切片截取字符串
        #     result = product[:char_count]
        #     print(result)
        #     for item in util_config.get("products"):
        #         if item["title"] in result:
        #             print("                   "+item["title"])
        #     return
        def on_mousewheel(event):
            mycanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # def on_button_click(title,Cost_label,Profit_label,unitPrice,sum):
        #     #browser.close()
        #     new_Cost = simpledialog.askstring("成本价", f"请{title}输入新的成本价1:")
        #     if new_Cost:
        #         Cost_label.config(text="成本价：" + new_Cost)
        #         Profit_label.config(text="利润：" + str((unitPrice-float(new_Cost))*sum))
        #         print(f"{title}新的成本价: {new_Cost}")
        #         products = util_config.get("products")
        #         sum = 0
        #         for item in products:
        #             if item["title"] == title:
        #                 item["Cost"]=new_Cost
        #                 print(item)
        #                 util_config.update_list("products",sum,item)
        #             sum+=1

        def on_button_click(title,Cost_label,Profit_label,unitPrice,sum,Cost):
            #browser.close()
            new_Cost = simpledialog.askstring("成本价", f"请{title}输入新的成本价:")
            if new_Cost:
                Cost_label.config(text="成本价：" + new_Cost)
                Profit_label.config(text="利润：" + str((unitPrice-float(new_Cost))*sum))
                print(f"{title}新的成本价: {new_Cost}")
                products = util_config.get("products")
                if Cost==0:
                    GUI.CumulativeCost += float(new_Cost)*sum
                    GUI.CumulativeProfit += (unitPrice-float(new_Cost))*sum
                    CumulativeProfitlabel.config(text="累计利润：" + str(GUI.CumulativeProfit))
                    CumulativeCostlabel.config(text="累计成本：" + str(GUI.CumulativeCost))
                else:
                    GUI.CumulativeCost -= Cost
                    GUI.CumulativeCost += float(new_Cost) * sum
                    GUI.CumulativeProfit -= (unitPrice - Cost) * sum
                    GUI.CumulativeProfit += (unitPrice - float(new_Cost)) * sum
                    CumulativeProfitlabel.config(text="累计利润：" + str(GUI.CumulativeProfit))
                    CumulativeCostlabel.config(text="累计成本：" + str(GUI.CumulativeCost))
                sum = 0
                for item in products:
                    if item["title"] == title:
                        item["Cost"]=new_Cost
                        print(item)
                        util_config.update_list("products",sum,item)
                    sum+=1

        #容器
        myframe.bind("<MouseWheel>", on_mousewheel)
        frame = Frame(myframe)
        #frame.place(x=0, y=y, width=500, height=90)
        frame.pack(anchor='w')
        frame.bind("<MouseWheel>", on_mousewheel)
        price_label = Label(frame, text="订单编号："+orderInfo['订单编号'], anchor="center", )
        #price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10,anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        price_label = Label(frame, text="顾客姓名：" + orderInfo['顾客姓名'], anchor="center", )
        # price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10, anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        price_label = Label(frame, text="顾客电话：" + orderInfo['顾客电话'], anchor="center", )
        # price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10, anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        price_label = Label(frame, text="本单预计收入：" + orderInfo['本单预计收入'], anchor="center", )
        # price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10, anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        price_label = Label(frame, text="本单顾客实际支付（已支付）：" + orderInfo['本单顾客实际支付（已支付）'], anchor="center", )
        # price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10, anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        price_label = Label(frame, text="商品：", anchor="center", )
        # price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10, anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)

        # 添加标签
        for order in orderInfo['商品']:
            product = order['name'].replace(order['Spec'], '')
            #percentage=50
            # if len(product)>34:
            #     percentage = 50

            # 计算要截取的字符数
            #char_count = int(len(product) * (percentage / 100))

            # 使用切片截取字符串
            result = re.sub(r'\（[^）]*\）$', '', product).rstrip()
            #print(result)
            for item in util_config.get("products"):


                # if str(order["unitPrice"].replace("¥", ""))!=formatted_float:
                #     continue
                #if item["title"] in result:
                if result == item["title"]:
                    string = item["price"]
                    if "-" in string:
                        numbers = string.split("-")
                        num1 = float(numbers[0])
                        num2 = float(numbers[1])
                        formatted_num1 = "{:.2f}".format(num1)
                        formatted_num2 = "{:.2f}".format(num2)
                        if float(order["unitPrice"].replace("¥", "")) < float(formatted_num1) or float(
                                order["unitPrice"].replace("¥", "")) > float(formatted_num2):
                            print("1                   " + order["unitPrice"].replace("¥", ""))
                            print("                   " + formatted_num1)
                            print("                   " + formatted_num2)
                            continue
                    # elif float("{:.2f}".format(float(string))) != float(order["unitPrice"].replace("¥", "")):
                    #     print("2                   " + order["unitPrice"].replace("¥", ""))
                    #     print("                   " + "{:.2f}".format(float(string)))
                    #     continue

                    #print("                   " + item["title"])
                    # print("0                   " + order["unitPrice"].replace("¥", ""))
                    # print("                   " + item["price"])
                    # 添加图片
                    framess = Frame(myframe)
                    # frame.place(x=0, y=y, width=500, height=90)
                    framess.pack(anchor='w')
                    framess.bind("<MouseWheel>", on_mousewheel)
                    image_path = "./image/" + item["image"]
                    img = Image.open(image_path)
                    img = img.resize((70, 70))  # 调整图片大小
                    img_tk = ImageTk.PhotoImage(img)
                    image_label = Label(framess, image=img_tk)
                    image_label.image = img_tk  # 保持对图像的引用，以防止被垃圾回收
                    # image_label.place(x=20, y=10)  # 设置图片的位置
                    image_label.pack(side=LEFT, padx=10)
                    image_label.bind("<MouseWheel>", on_mousewheel)

                    text = item["title"]
                    text_label = Label(framess, text=text)
                    # text_label.place(x=100, y=10, width=378, height=30)
                    text_label.pack(side=TOP, padx=10,anchor='w')
                    text_label.bind("<MouseWheel>", on_mousewheel)

                    price_label = Label(framess, text="价格："+item["price"], anchor="center", )
                    #price_label.place(x=100, y=50, width=100, height=30)
                    price_label.pack(side=LEFT, padx=10,anchor='w')
                    price_label.bind("<MouseWheel>", on_mousewheel)

                    stock_label = Label(framess, text="库存："+item["stock"], anchor="center", )
                    #stock_label.place(x=200, y=50, width=100, height=30)
                    stock_label.pack(side=LEFT,anchor='w')
                    stock_label.bind("<MouseWheel>", on_mousewheel)

                    stock_label = Label(framess, text="数量：" + order['sum'], anchor="center", )
                    # stock_label.place(x=200, y=50, width=100, height=30)
                    stock_label.pack(side=LEFT, anchor='w')
                    stock_label.bind("<MouseWheel>", on_mousewheel)

                    stock_label = Label(framess, text="小计：" + order['subtotal'], anchor="center", )
                    # stock_label.place(x=200, y=50, width=100, height=30)
                    stock_label.pack(side=LEFT, anchor='w')
                    stock_label.bind("<MouseWheel>", on_mousewheel)

                    if item.get("Cost"):
                        Cost_label = Label(framess, text="成本价：" + item['Cost'], anchor="center", )
                        # stock_label.place(x=200, y=50, width=100, height=30)
                        Cost_label.pack(side=LEFT, anchor='w')
                        Cost_label.bind("<MouseWheel>", on_mousewheel)
                        #累计成本
                        GUI.CumulativeCost+=float(item['Cost'])*int(order['sum'].replace("x", ""))
                        Profit = (float(order["unitPrice"].replace("¥", ""))-float(item['Cost']))*int(order['sum'].replace("x", ""))
                        # 累计利润
                        GUI.CumulativeProfit+=Profit
                        Profit_label = Label(framess, text="利润："+str(Profit), anchor="center", )

                        btn = Button(framess, text="修改成本价", takefocus=False, )
                        btn.pack(side=LEFT, anchor='w')
                        btn.bind("<Button-1>", lambda event, title=item["title"],Cost_label=Cost_label,Profit_label=Profit_label,unitPrice=float(order["unitPrice"].replace("¥", "")),sum=int(order['sum'].replace("x", "")),Cost=item['Cost']: on_button_click(title,Cost_label,Profit_label,unitPrice,sum,Cost))
                        btn.bind("<MouseWheel>", on_mousewheel)

                        # stock_label.place(x=200, y=50, width=100, height=30)
                        Profit_label.pack(side=LEFT, anchor='w')
                        Profit_label.bind("<MouseWheel>", on_mousewheel)
                    else:
                        Cost_label = Label(framess, text="成本价：", anchor="center", )
                        # stock_label.place(x=200, y=50, width=100, height=30)
                        Cost_label.pack(side=LEFT, anchor='w')
                        Cost_label.bind("<MouseWheel>", on_mousewheel)

                        Profit_label = Label(framess, text="利润：请添加成本价", anchor="center", )

                        btn = Button(framess, text="添加成本价", takefocus=False, )
                        btn.pack(side=LEFT, anchor='w')
                        btn.bind("<Button-1>", lambda event, title=item["title"],Cost_label=Cost_label,Profit_label=Profit_label,unitPrice=float(order["unitPrice"].replace("¥", "")),sum=int(order['sum'].replace("x", "")),Cost=0: on_button_click(title,Cost_label,Profit_label,unitPrice,sum,Cost))
                        btn.bind("<MouseWheel>", on_mousewheel)

                        # stock_label.place(x=200, y=50, width=100, height=30)
                        Profit_label.pack(side=LEFT, anchor='w')
                        Profit_label.bind("<MouseWheel>", on_mousewheel)
                    CumulativeProfitlabel.config(text="累计利润：" + str(GUI.CumulativeProfit))
                    CumulativeCostlabel.config(text="累计成本：" + str(GUI.CumulativeCost))

                    #Cost_labellist[item["title"]]=Cost_label
        frame = Frame(myframe)
        # frame.place(x=0, y=y, width=500, height=90)
        frame.pack(anchor='w')
        frame.bind("<MouseWheel>", on_mousewheel)
        price_label = Label(frame, text="    ", anchor="center", )
        # price_label.place(x=100, y=50, width=100, height=30)
        price_label.pack(side=TOP, padx=10, anchor='w')
        price_label.bind("<MouseWheel>", on_mousewheel)
        # price_label = Label(frame, text="价格："+pro["price"], anchor="center", )
        # #price_label.place(x=100, y=50, width=100, height=30)
        # price_label.pack(side=LEFT, padx=10,anchor='w')
        # price_label.bind("<MouseWheel>", on_mousewheel)
        #
        # stock_label = Label(frame, text="库存："+pro["stock"], anchor="center", )
        # #stock_label.place(x=200, y=50, width=100, height=30)
        # stock_label.pack(side=LEFT,anchor='w')
        # stock_label.bind("<MouseWheel>", on_mousewheel)

    #GUI.GUImain(order_info)

def jiankong():
    global urllist
    global iscontinue
    global browser
    caps = {
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY',
        'goog:loggingPrefs': {'performance': 'ALL'},  # 记录性能日志
        'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}  # 无界面模式
    }
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    #options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=r".\chromedriver-win64\chromedriver.exe", options=options,desired_capabilities=caps)
    browser.minimize_window()
    # try:
    #     browser.get("https://shangoue.meituan.com/#/page/order#/order/allHistory")
    #     time.sleep(3)
    #     current_url = browser.current_url
    #     print(current_url)
    #     if current_url=="https://waimaie.meituan.com/new_fe/login_gw#/login":
    #         try:
    #             element = browser.find_element(by=By.XPATH, value="//input[@id='login']")
    #             element.send_keys("wmcxyc623917")
    #             element = browser.find_element(by=By.XPATH, value="//input[@id='password']")
    #             element.send_keys("BeiTai2023")
    #             time.sleep(1)
    #             element = browser.find_element(by=By.XPATH, value="//div[@class='ep-checkbox-container']")
    #             element.click()
    #         except Exception as e:
    #             print("没有该元素！：",e)
    #             pass
    #     try:
    #         mask = browser.find_element(By.XPATH, "//div[@class='boo-modal-mask']")
    #         browser.execute_script("arguments[0].style.display= 'none';", mask)
    #         wrap = browser.find_element(By.XPATH, "//div[@class='boo-modal-wrap']")
    #         browser.execute_script("arguments[0].classList.add('boo-modal-hidden')", wrap)
    #         # actions = ActionChains(browser)
    #         # # 在空白区域上模拟鼠标点击
    #         # actions.click(popup)
    #     except Exception as e:
    #         print("没有遮挡元素！")
    #         pass
    #     time.sleep(3)
    #     menu_items = browser.find_elements(by=By.XPATH, value="//li[@class='roo-plus-menu-sub']")
    #     if len(menu_items) > 1:
    #         # 触发第二个元素的点击事件
    #         menu_items[1].click()
    #         print("订单管理！")
    #     else:
    #         print("没有找到第二个class为'roo-plus-menu-sub'的li元素")
    #     #menu_items.click()
    #     time.sleep(3)
    #     iframe_element = browser.find_element(by=By.XPATH, value="//iframe[@id='hashframe']")
    #     browser.switch_to.frame(iframe_element)
    #     OrderList = browser.find_elements(by=By.XPATH, value="//div[@class='order-card-container divide-line']")
    #     print("订单详情！")
    #     #print(OrderList)
    #     processOrders(OrderList)
    #
    # except Exception as e:
    #     print("打开错误！：",e)
    #     pass
    browser.get("https://shangoue.meituan.com/#/page/order#/order/allHistory")
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
    menu_items = browser.find_elements(by=By.XPATH, value="//li[@class='roo-plus-menu-sub']")
    if len(menu_items) > 1:
        # 触发第二个元素的点击事件
        menu_items[1].click()
        print("订单管理！")
    else:
        print("没有找到第二个class为'roo-plus-menu-sub'的li元素")
    # menu_items.click()
    time.sleep(3)





    iframe_element = browser.find_element(by=By.XPATH, value="//iframe[@id='hashframe']")
    browser.switch_to.frame(iframe_element)

    Productslist = browser.find_element(by=By.XPATH, value="//div[@class='order-pagination-wrapper']")
    # Products = Productslist.find_element(by=By.XPATH, value="//tbody[@class='boo-table-tbody']")
    time.sleep(1)
    ul = Productslist.find_element(by=By.XPATH, value="//ul[@class='roo-pagination']")
    li = ul.find_elements(by=By.XPATH, value="//li")
    sum = 1
    for i in li:
        try:
            sum = int(i.text) if int(i.text) > sum else sum
        except Exception as e:
            pass
    print("共", sum, "页")
    for i in range(0, sum):
        if iscontinue:
            print("结束线程！")
            browser.close()
            return
        print('第', i + 1, '页')
        time.sleep(3)
        OrderList = browser.find_elements(by=By.XPATH, value="//div[@class='order-card-container divide-line']")
        print("订单详情！")
        # print(OrderList)
        processOrders(OrderList)
        time.sleep(1)
        try:
            ul = Productslist.find_element(by=By.XPATH, value="//ul[@class='roo-pagination']")
            li = ul.find_element(by=By.XPATH, value="//li[@class='arrow']")
            li.click()
        except Exception as e:
            print("没有下一页了！")
            pass
    print("爬取完毕！")
    browser.close()
    return










def main(frame,canvas,Costlabel,Profitlabel):
    global myframe
    global mycanvas
    global iscontinue
    global CumulativeCostlabel
    global CumulativeProfitlabel
    iscontinue = False
    myframe = frame
    mycanvas = canvas
    CumulativeCostlabel = Costlabel
    CumulativeProfitlabel = Profitlabel
    thread = threading.Thread(target=openChrome)
    thread.start()
    thread2 = threading.Thread(target=jiankong)
    thread2.start()



if __name__ == "__main__":
    main()
