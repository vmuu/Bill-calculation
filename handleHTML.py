from bs4 import BeautifulSoup

def handleHTML(html_doc):

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_doc, 'lxml')

    # 解析订单信息
    orders = soup.find_all('div', class_='order-card-container divide-line')[0]

    order_info = {}
    #print(orders)
    # 订单编号
    order_id = orders.find('p', class_='order-num font_sf_heavy')
    order_info['订单编号'] = order_id.get_text(strip=True) if order_id else "未提供"

    # 下单时间
    # order_time = orders.find('div', class_='order-time')
    # order_info['下单时间'] = order_time.get_text(strip=True) if order_time else "未提供"

    # 顾客信息
    customer_info = orders.find('section', class_='general-users-container')
    if customer_info:
        customer_name = customer_info.find('div', style_='height: 6px; width: 6px; border-radius: 50%; margin-right: 8px; background: rgb(34, 34, 34);')
        order_info['顾客姓名'] = customer_name.get_text(strip=True) if customer_name else "未提供"

        customer_phone = customer_info.find('p', class_='mb-6')
        order_info['顾客电话'] = customer_phone.get_text(strip=True) if customer_phone else "未提供"

    # 商品信息
    product_info = orders.find('section', class_='product-list')
    if product_info:
        # products = product_info.find_all('span', class_='goods-name')
        # order_info['商品'] = [product.get_text(strip=True) for product in products]
        products = product_info.find_all('div', class_='product-goods-item flex-between medium')
        order_info['商品'] = []
        for product in products:
            name = product.find_all('span', class_='goods-name')[0].get_text(strip=True)
            unitPrice = product.find_all('span', class_='goods-num')[0].get_text(strip=True)
            sum = product.find_all('span', class_='goods-num')[1].get_text(strip=True)
            subtotal = product.find_all('span', class_='goods-num')[2].get_text(strip=True)
            try:
                Spec = "（"+product.find_all('p')[1].get_text(strip=True).split(" ", 1)[1]+"）"
            except Exception as e:
                Spec = ""
            order_info['商品'].append({"name":name,"unitPrice":unitPrice,"sum":sum,"subtotal":subtotal,"Spec":Spec})

    # 本单预计收入
    product_info = orders.find('div', class_='total')
    if product_info:
        # 本单顾客实际支付（已支付）
        font_sf_bold = product_info.find_all('span', class_='expect-amount font_sf_bold')[0]
        order_info['本单预计收入'] = font_sf_bold.get_text(strip=True) if font_sf_bold else "未提供"
        font_sf_semibold = product_info.find_all('span', class_='actual-amount font_sf_semibold')[0]
        order_info['本单顾客实际支付（已支付）'] = font_sf_semibold.get_text(strip=True) if font_sf_semibold else "未提供"


    # 打印订单信息
    # print(order_info)
    # print("订单编号",order_info['订单编号'])
    # print("顾客姓名",order_info['顾客姓名'])
    # print("顾客电话",order_info['顾客电话'])
    # print("商品",order_info['商品'])
    # print("本单预计收入",order_info['本单预计收入'])
    # print("本单顾客实际支付（已支付）",order_info['本单顾客实际支付（已支付）'])
    # print()
    return order_info

    # for order in orders:
    #     order_info = {}
    #
    #     # 订单编号
    #     order_id = order.find('div', class_='order-id')
    #     order_info['订单编号'] = order_id.get_text(strip=True) if order_id else "未提供"
    #
    #     # 下单时间
    #     order_time = order.find('div', class_='order-time')
    #     order_info['下单时间'] = order_time.get_text(strip=True) if order_time else "未提供"
    #
    #     # 顾客信息
    #     customer_info = order.find('div', class_='customer-info')
    #     if customer_info:
    #         customer_name = customer_info.find('div', class_='customer-name')
    #         order_info['顾客姓名'] = customer_name.get_text(strip=True) if customer_name else "未提供"
    #
    #         customer_phone = customer_info.find('div', class_='customer-phone')
    #         order_info['顾客电话'] = customer_phone.get_text(strip=True) if customer_phone else "未提供"
    #
    #     # 商品信息
    #     product_info = order.find('div', class_='product-info')
    #     if product_info:
    #         products = product_info.find_all('div', class_='product-item')
    #         order_info['商品'] = [product.get_text(strip=True) for product in products]
    #
    #     # 打印订单信息
    #     print(order_info)

    # 你可以根据需要进一步处理或保存这些信息
