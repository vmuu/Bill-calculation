from tkinter import *
from tkinter.ttk import *
from tkinter import Tk, messagebox
import sys
import fetchProducts
from PIL import ImageTk, Image
import util_config
import main
from tkinter import simpledialog
from platforms import get_cpu_id
import hashlib

HardwareID = "01FF435281724067F99E8F2E124E0371"


mycanvas=None
myframe=None
mycanvas2=None
myframe2=None
CumulativeProfit=0
CumulativeCost=0
CumulativeProfitlabel=None
CumulativeCostlabel=None

def updateframe(frame,canvas):
    # 更新滚动区域大小
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))



class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_llg1eqdt = self.__tk_label_llg1eqdt(self)
        self.tk_frame_llj6z2rx = self.__tk_frame_llj6z2rx(self)
        self.tk_text_lpgllhbl = self.__tk_text_lpgllhbl(self.tk_frame_llj6z2rx)
        self.tk_button_llzzuw1t = self.__tk_button_llzzuw1t(self)
        self.tk_button_lpjkv3vv = self.__tk_button_lpjkv3vv(self)
        self.tk_frame_lpjlfcdb = self.__tk_frame_lpjlfcdb(self)
        self.tk_frame_lpjlg48a = self.__tk_frame_lpjlg48a(self)
        self.tk_label_lpjml2cw = self.__tk_label_lpjml2cw(self)
        #self.tk_canvas_lpjmyays = self.__tk_canvas_lpjmyays(self.tk_frame_lpjlfcdb)
        self.tk_button_lpkq1dkq = self.__tk_button_lpkq1dkq(self)
        #self.tk_button_jisuan = self.__tk_button_jisuan(self)
        self.tk_label_lpo7bk30 = self.__tk_label_lpo7bk30(self)
        self.tk_label_lpo7cb81 = self.__tk_label_lpo7cb81(self)

    def __win(self):
        self.title("账目整理")
        # 设置窗口大小、居中
        width = 1301
        height = 800
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def redirect_stdout_to_text_widget(self, text_widget):
        class StdoutRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget

            def write(self, message):
                self.text_widget.insert(END, message)
                self.text_widget.see(END)

            def flush(self):
                # 这里没有实际刷新操作，因为 Text 小部件不需要它
                pass

        sys.stdout = StdoutRedirector(text_widget)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)


    def __tk_label_llg1eqdt(self, parent):
        label = Label(parent, text="执行信息：", anchor="center")
        label.place(x=20, y=10, width=60, height=30)
        return label

    def __tk_frame_llj6z2rx(self, parent):
        frame = Frame(parent)
        frame.place(x=20, y=40, width=740, height=377)
        return frame

    def __tk_text_lpgllhbl(self, parent):
        text = Text(parent)
        text.place(x=20, y=20, width=699, height=339)
        return text

    def __tk_button_llzzuw1t(self, parent):
        btn = Button(parent, text="更新商品库", takefocus=False)
        btn.place(x=780, y=10, width=77, height=30)
        return btn

    def __tk_button_lpjkv3vv(self, parent):
        btn = Button(parent, text="结束更新", takefocus=False, )
        btn.place(x=880, y=10, width=78, height=30)
        return btn



    def __tk_frame_lpjlfcdb(self,parent):
        global mycanvas
        global myframe
        # 创建 Frame 作为容器
        container = Frame(parent)
        container.place(x=780, y=80, width=499, height=679)
        container.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        # 创建 Canvas 和 Scrollbar
        canvas = Canvas(container)
        vbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        hbar = Scrollbar(container, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        def on_mousewheel(event, canvas):
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

        canvas.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        # 放置 Canvas 和 Scrollbar
        vbar.pack(side="right", fill="y")
        hbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        # 创建一个 Frame 作为 Canvas 的子窗口
        self.inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        updateframe(self.inner_frame,canvas)
        mycanvas = canvas
        myframe = self.inner_frame
        productslist = util_config.get("products")
        print("productslist长度：",len(productslist))
        if productslist != None:
            for item in productslist:
                frame = Frame(self.inner_frame)
                # frame.place(x=0, y=y, width=500, height=90)
                frame.pack(anchor='w')
                frame.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
                Image.MAX_IMAGE_PIXELS = 100000000
                # 添加图片
                image_path = "./image/" + item["image"]
                img = Image.open(image_path)
                img = img.resize((70, 70))  # 调整图片大小
                img_tk = ImageTk.PhotoImage(img)
                image_label = Label(frame, image=img_tk)
                image_label.image = img_tk  # 保持对图像的引用，以防止被垃圾回收
                # image_label.place(x=20, y=10)  # 设置图片的位置
                image_label.pack(side=LEFT, padx=10)
                image_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                # 添加标签
                text = item["title"]
                text_label = Label(frame, text=text)
                # text_label.place(x=100, y=10, width=378, height=30)
                text_label.pack(side=TOP)
                text_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                price_label = Label(frame, text="价格：" + item["price"], anchor="center", )
                # price_label.place(x=100, y=50, width=100, height=30)
                price_label.pack(side=LEFT, padx=10, anchor='w')
                price_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                stock_label = Label(frame, text="库存：" + item["stock"], anchor="center", )
                # stock_label.place(x=200, y=50, width=100, height=30)
                stock_label.pack(side=LEFT, anchor='w')
                stock_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                if item.get("Cost"):
                    Cost_label = Label(frame, text="成本价：" + item["Cost"], anchor="center", )
                    # stock_label.place(x=200, y=50, width=100, height=30)
                    Cost_label.pack(side=LEFT, anchor='w')
                    Cost_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                    btn = Button(frame, text="修改成本价", takefocus=False, )
                    btn.pack(side=LEFT, anchor='w')
                    btn.bind("<Button-1>", lambda event, title=item["title"], Cost_label=Cost_label: on_button_click(title,Cost_label))
                    btn.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
                else:
                    Cost_label = Label(frame, text="成本价：", anchor="center", )
                    # stock_label.place(x=200, y=50, width=100, height=30)
                    Cost_label.pack(side=LEFT, anchor='w')
                    Cost_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

                    btn = Button(frame, text="添加成本价", takefocus=False, )
                    btn.pack(side=LEFT, anchor='w')
                    btn.bind("<Button-1>",
                             lambda event, title=item["title"], Cost_label=Cost_label: on_button_click(title,
                                                                                                       Cost_label))
                    btn.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

        return container

    # def __tk_canvas_lpjmyays(self, parent):
    #     canvas = Canvas(parent)  # 创建Canvas组件
    #     canvas.place(x=0, y=0, relwidth=1, relheight=1)
    #
    #     # 在此处添加你想要放置在canvas中的组件
    #
    #     # 创建垂直滚动条和水平滚动条对象
    #     vbar = Scrollbar(parent, orient="vertical")
    #     hbar = Scrollbar(parent, orient="horizontal")
    #
    #     # 将滚动条与Canvas的滚动命令相关联
    #     canvas.configure(yscrollcommand=vbar.set)
    #     canvas.configure(xscrollcommand=hbar.set)
    #
    #     # 配置滚动条的命令
    #     vbar.config(command=canvas.yview)
    #     hbar.config(command=canvas.xview)
    #
    #     # 设置滚动条的位置和尺寸
    #     vbar.place(relx=1, rely=0, relheight=1, anchor='ne')
    #     hbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
    #
    #     # 调用create_bar方法自动隐藏滚动条并响应鼠标移入移出事件
    #     self.create_bar(parent, canvas, is_vbar=True, is_hbar=True, x=780, y=80, w=499, h=670, pw=780, ph=759)
    #     return canvas

    def __tk_frame_lpjlg48a(self,parent):
        global mycanvas2
        global myframe2
        # 创建 Frame 作为容器
        container = Frame(parent)
        container.place(x=20, y=440, width=739, height=319)

        # 创建 Canvas 和 Scrollbar
        canvas = Canvas(container)
        vbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        hbar = Scrollbar(container, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        def on_mousewheel(event, canvas):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        # 放置 Canvas 和 Scrollbar
        vbar.pack(side="right", fill="y")
        hbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        # 创建一个 Frame 作为 Canvas 的子窗口
        self.inner_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        updateframe(self.inner_frame, canvas)
        mycanvas2 = canvas
        myframe2 = self.inner_frame
        # productslist = util_config.get("products")
        # if productslist != None:
        #     for item in productslist:
        #         frame = Frame(self.inner_frame)
        #         # frame.place(x=0, y=y, width=500, height=90)
        #         frame.pack(anchor='w')
        #         frame.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        #         Image.MAX_IMAGE_PIXELS = 100000000
        #         # 添加图片
        #         image_path = "./image/" + item["image"]
        #         img = Image.open(image_path)
        #         img = img.resize((70, 70))  # 调整图片大小
        #         img_tk = ImageTk.PhotoImage(img)
        #         image_label = Label(frame, image=img_tk)
        #         image_label.image = img_tk  # 保持对图像的引用，以防止被垃圾回收
        #         # image_label.place(x=20, y=10)  # 设置图片的位置
        #         image_label.pack(side=LEFT, padx=10)
        #         image_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        #
        #         # 添加标签
        #         text = item["title"]
        #         text_label = Label(frame, text=text)
        #         # text_label.place(x=100, y=10, width=378, height=30)
        #         text_label.pack(side=TOP)
        #         text_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        #
        #         price_label = Label(frame, text="价格：" + item["price"], anchor="center", )
        #         # price_label.place(x=100, y=50, width=100, height=30)
        #         price_label.pack(side=LEFT, padx=10, anchor='w')
        #         price_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
        #
        #         stock_label = Label(frame, text="库存：" + item["stock"], anchor="center", )
        #         # stock_label.place(x=200, y=50, width=100, height=30)
        #         stock_label.pack(side=LEFT, anchor='w')
        #         stock_label.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

        return container

    def __tk_label_lpjml2cw(self,parent):
        label = Label(parent,text="商品库",anchor="center", )
        label.place(x=780, y=50, width=50, height=30)
        return label

    def __tk_button_lpkq1dkq(self,parent):
        btn = Button(parent, text="获取今日订单账目", takefocus=False,)
        btn.place(x=980, y=10, width=119, height=30)
        return btn

    def __tk_button_jisuan(self,parent):
        btn = Button(parent, text="计算今日订单账目", takefocus=False,)
        btn.place(x=1110, y=10, width=119, height=30)
        return btn

    def __tk_label_lpo7bk30(self,parent):
        global CumulativeCostlabel
        CumulativeCostlabel = Label(parent,text="累计成本：",anchor="center", )
        CumulativeCostlabel.place(x=20, y=770, width=159, height=30)
        return CumulativeCostlabel

    def __tk_label_lpo7cb81(self,parent):
        global CumulativeProfitlabel
        CumulativeProfitlabel = Label(parent,text="累计利润：",anchor="center", )
        CumulativeProfitlabel.place(x=200, y=770, width=160, height=30)
        return CumulativeProfitlabel

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.redirect_stdout_to_text_widget(self.tk_text_lpgllhbl)  # 将控制台输出重定向到Text小部件

    def productDatabase(self, evt):
        result = messagebox.askyesno("确认框", "自动更新商品库如果商品名更改过，该商品的新数据将不会写入到数据文件中！")
        # 根据用户的选择做出相应的处理
        if result:
            fetchProducts.main(myframe,mycanvas)
            print("正在启动更新程序！")
            for widget in myframe.winfo_children():
                widget.destroy()
        else:
            print("取消操作！")

    def StopThread(self, evt):
        if fetchProducts.iscontinue:
            print("更新程序没有运行！")
            return
        else:
            result = messagebox.askyesno("确认框", "确定取消更新吗？（取消更新会导致商品库数据不全！）")
            # 根据用户的选择做出相应的处理
            if result:
                fetchProducts.iscontinue=True
                print("正在结束进程！")
            else:
                print("取消操作！")

    def calculateAccounts(self,evt):
        global CumulativeProfit
        global CumulativeCostlabel
        CumulativeProfit = 0
        CumulativeCostlabel = 0
        #print("<Button-1>事件未处理:",evt)
        for widget in myframe2.winfo_children():
            widget.destroy()
        main.main(myframe2,mycanvas2,self.tk_label_lpo7bk30,self.tk_label_lpo7cb81)

    def jisuan(self,evt):
        #self.tk_text_lpgllhbl.delete("1.0", "end")
        #print("<Button-1>事件未处理:",main.order_info)
        for item in main.order_info:
            item["商品"]


    def __event_bind(self):
        self.tk_button_llzzuw1t.bind('<Button-1>', self.productDatabase)
        self.tk_button_lpjkv3vv.bind('<Button-1>',self.StopThread)
        self.tk_button_lpkq1dkq.bind('<Button-1>',self.calculateAccounts)
        #self.tk_button_jisuan.bind('<Button-1>',self.jisuan)
        pass

def initwin():
    ID = get_cpu_id()
    m = hashlib.md5()
    m.update(ID.encode(encoding='UTF-8'))
    encrypted_result = m.hexdigest().upper()
    #print(ID)
    #print(encrypted_result)
    if encrypted_result != HardwareID:
        messagebox.showwarning("警告", "没有使用权限！")
        return
    util_config.init_conf()
    win = Win()
    win.mainloop()

if __name__ == "__main__":
    initwin()
    #pyinstaller -F -i favicon.ico program.py
    #pyinstaller -F GUI.py
