import random
import sys

import requests
from lxml import etree
from hyper.contrib import HTTP20Adapter
import datetime
import time
import traceback


def get_boc_hk_currency():
    url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
    params = {'erectDate': None, 'nothing': None, 'pjname': '英镑', 'head': 'head_620.js', 'bottom': 'bottom_591.js',
              't': random.random()}

    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url, params=params)

    dom = etree.HTML(res.text)
    tds = dom.xpath('/html/body//div[@class="BOC_main publish"]//tr[2]/td')
    # /html/body/div[1]/div[4]/table/tbody/tr[21]
    # 购汇
    buy_currency = round(float(tds[3].text) / 100, 4)
    # 结汇
    sale_currency = round(float(tds[1].text) / 100, 4)
    return buy_currency, sale_currency


if __name__ == '__main__':
    # 记录上一次购汇发送的汇率和时间
    last_boc_buy_currency = -1
    last_boc_sale_currency = -1
    last_time = '初始化运行无数据，已记录本次'

    while True:
        try:
            boc_buy_currency, boc_sale_currency = get_boc_hk_currency()
            print(str(datetime.datetime.now()) + ' ' + str(boc_buy_currency) + ' ' + str(boc_sale_currency))
            if last_boc_buy_currency == -1 or last_boc_buy_currency != boc_buy_currency:
                print("监测到变化。")
                cur_time = str(datetime.datetime.now())
                print(f'''
                {cur_time}
                [boc购汇]\t{boc_buy_currency}
                [boc结汇]\t{boc_sale_currency}
                -------------------
                (上一次中银购汇汇率)
                {last_time}
                {last_boc_buy_currency}
                ''')
                last_boc_buy_currency = boc_buy_currency
                last_boc_sale_currency = boc_sale_currency
                last_time = str(cur_time)
        except BaseException as e:
            traceback.print_exc()
        finally:
            sys.stdout.flush()
            time.sleep(3000 - random.randint(-9, 9))
