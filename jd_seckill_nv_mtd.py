#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
使用说明
依赖： requests, time, json

使用配置：只要填这5个 1.cookie 2.商品url 3.秒杀时间 4.秒杀总次数限制 5.秒杀请求间隙
示例：
self.thor = '获取我的订单页面的cookie'
self.goods_url = 'https://item.jd.com/100009514841.html'
self.order_time = '2020-12-01 10:00:00.0'
self.retry_limit = 1
self.gap = 0.2
注意：
使用前，去京东设置一下，取消默认使用红包、京豆，否则需要输入支付密码，影响下单。
'''

import requests
import time
import json
import _thread
import copy

#日志模板，有颜色和状态
LOG_TEMPLE_BLUE='\033[1;34m{}\033[0m '
LOG_TEMPLE_RED='\033[1;31m{}\033[0m '
LOG_TEMPLE_SUCCESS='\033[1;32mSUCCESS\033[0m '
LOG_TEMPLE_FAILED='\033[1;31mFAILED\033[0m '

class JD:
    headers = {
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    def __init__(self):
        # 配置项 只要填这5个 1.cookie 2.url 3.秒杀时间 4.秒杀总次数限制 5.秒杀请求间隙
        self.thor = '__jdu=16049717216091655289323; shshshfpa=7afba311-a083-0ca3-33ee-65ccb783093e-1605773770; pinId=08cnJ_-psDnBJqKyyYWCow; pin=libiao8668; unick=%E7%94%B5%E8%9A%8A%E6%8B%8D00; _tp=UJXNhVYh4nWfxAn3m8QLww%3D%3D; _pst=libiao8668; shshshfpb=b%20fMyExgX1XvkdR0xo1FaHg%3D%3D; user-key=8a3131e6-deb0-4105-90f9-66160136130c; areaId=2; ipLocation=%u4e0a%u6d77; ipLoc-djd=2-2830-51806-0.137564193; cn=3; unpl=V2_ZzNtbRcHRxx9XxZTfk5YV2IEQFUSVRETcA4TAHlKXgY0BxdUclRCFnQURldnGF8UZwUZWEJcRhNFCEdkexhdBW4AGl9DVXMlRQtGZHopXAJmBhpbQlFAFXIJTlR8HVgGbgsQXkBncxV9DHZUehhdBWAAFFxHVUQlI1YTVH4fbAVvBRZbQ1VDHXU4R2R6KQprZwITXENWQhZ9DgtUfBhZDWEDFF5CUEIddQ9CUHgQVAdkASJcclQ%3d; __jdv=122270672|xcx.ubja.vip|t_1001829303_|tuiguang|da589fa64f5c46c9a3c747de3b32b548|1606902107919; ceshi3.com=201; PCSYCityID=CN_310000_310100_310115; shshshfp=6ed72a218f03b1d3e8b07d42791ed0d3; shshshsID=e60a1481135769728f81270269f741cf_1_1607063084874; __jda=122270672.16049717216091655289323.1604971722.1606961703.1607063083.27; __jdc=122270672; 3AB9D23F7A4B3C9B=ALMB2BH7TWEPNC33LW2SUXB7U27CV7AQMOWZPB7SBJMYZGYSOIDF54HQ3J7YRR57KLMVNSBNOYDQFI2K6AIE4O64DY; wlfstk_smdl=3jf0okmky6lgru7blxzd2vv5fqcis9uv; TrackID=16moMh_zhKqRCiv9SH5Hzf3IelxOhS931jAqUSr52b8jJKT0dP1XetDoKBvh545_-LWNqhU7uZ7QYH6Nte7hCIr07IcT4szmgQSHDK06MLaY; thor=515642404184BA4F138DAB78E0533C79E15C96CE5B8DE4F65D2950CBD980A509B42A137668B1F671C0B891AE9F5CFE92AD98F8FC3637ABD765A86FCCEF0E40682975577D54EFF69E6CDDB52CA81A564E0199E7A446216AAC02BF88164031DC6BA3DBF9A6EC57905F0B2B83BBE82061BC9FB2299A37820728C7533DB526438BFCA547F1990F32D2E0B69DE34432BB050F; __jdb=122270672.6.16049717216091655289323|27.1607063083'
        # 七彩虹3080 ultra
        self.goods_url = 'https://item.jd.com/100015521042.html'
        self.order_time = '2020-12-04 15:00:00.0'
        # 七彩虹3080 ultra w
        self.goods_url = 'https://item.jd.com/100009044025.html'
        self.order_time = '2020-12-04 15:00:00.0'
        # 七彩虹3080 战斧
        #self.goods_url = 'https://item.jd.com/100015062660.html'
        #self.order_time = '2020-12-04 15:00:00.0'
        # 影驰黑将5499
        #self.goods_url = 'https://item.jd.com/100015325218.html'
        #self.order_time = '2020-11-27 10:00:00.0'
        # 盈通6800xt
        #self.goods_url = 'https://item.jd.com/100016642488.html'
        #self.order_time = '2020-11-27 10:00:00.0'
        # 蓝宝石6800xt
        #self.goods_url = 'https://item.jd.com/100016553676.html'
        #self.order_time = '2020-12-01 15:00:00.0'
        # 技嘉6800xt
        #self.goods_url = 'https://item.jd.com/100009514841.html'
        #self.order_time = '2020-12-04 10:00:00.0'
        self.goods_list = [
            {
                'goods_name': ' 七彩虹3080 ultra',
                'goods_url': 'https://item.jd.com/100015521042.html',
                'order_time':  '2020-12-04 15:00:00.0'
            }
            , {
                'goods_name': ' 七彩虹3080 ultra w',
                'goods_url': 'https://item.jd.com/100009044025.html',
                'order_time':  '2020-12-04 15:00:00.0'
            }
            #, {
            #     'goods_name': ' 七彩虹3080 战斧',
            #     'goods_url': 'https://item.jd.com/100015062660.html',
            #     'order_time':  '2020-12-04 15:00:00.0'
            # }
        ]
        # 次数设定
        self.retry_limit = 1
        # 间隔设定
        self.gap = 0.01

        self.user_info = ''
        self.index = 'https://www.jd.com/'
        # 用户信息获取地址
        self.user_url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?&callback=jsonpUserinfo&_=' + \
            str(int(time.time() * 1000))
        # 加购物车
        self.buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'
        # 修改购物车商品数量为1
        self.change_num = 'https://cart.jd.com/changeNum.action?pid={}&pcount=1&ptype=1'
        # 下单
        self.pay_url = 'https://cart.jd.com/gotoOrder.action'
        # 订单提交
        self.pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'
        self.goods_id = ''
        self.session = requests.session()

        # 重试计数
        self.retry_count = 0

        timeArray = time.strptime(self.order_time, "%Y-%m-%d %H:%M:%S.%f")
        self.order_time_st = int(time.mktime(timeArray))

    def login(self):
        JD.headers['referer'] = 'https://cart.jd.com/cart.action'
        c = requests.cookies.RequestsCookieJar()
        c.set('thor', self.thor)
        self.session.cookies.update(c)
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip('jsonpUserinfo()\n')
        user_info = json.loads(response)
        self.user_info = user_info
        print('账号：', user_info.get('nickName'))
        #if user_info.get('nickName'):
        #    while self.retry_limit > 0:
        #        time.sleep(self.gap)
        #        # 当前时间
        #        cur_time = time.time()
        #        if cur_time < self.order_time_st:
        #            print('\r'+' 抢购时间：', self.order_time, '剩余时间：',
        #                  round(self.order_time_st - cur_time, 2), '秒...', end='', flush=True)
        #            continue
        #        else:
        #            print("执行抢购，第", self.retry_count, "次重试")
        #            try:
        #                self.shopping()
        #                self.retry_limit = self.retry_limit - 1
        #                # 重试计数
        #                self.retry_count += 1
        #            except BaseException as be:
        #                be.with_traceback()
        #                continue
        #            pass
        # 多线程抢购
        if user_info.get('nickName'):
            # 遍历预约成功的商品，挨个抢购
            for goods in self.goods_list:
                item = copy.copy(self)
                # 下单时间（使用本机时间，记得和京东服务器同步时间）
                timeArray = time.strptime(goods['order_time'], "%Y-%m-%d %H:%M:%S.%f")
                order_time_st = int(time.mktime(timeArray))
                item.order_time_st = order_time_st
                goods['order_time_st'] = order_time_st
                item.goods_name = goods['goods_name']
                item.goods_url = goods['goods_url']
                item.order_time = goods['order_time']
                # 创建线程
                try:
                    _thread.start_new_thread(self.run, (item, ))
                except BaseException as be:
                    print ("Error: 无法启动线程")
                    be.with_traceback()
                pass
            pass
    # 为线程定义一个函数
    def run(self, item):
        #while True:
        #    time.sleep(item.gap)
        #    cur_time = time.time()
        #    print(item)
        #    if cur_time <= item.order_time_st:
        #        print('\r'+' 抢购时间：', self.order_time, '剩余时间：',
        #                round(self.order_time_st - cur_time, 2), '秒...', end='', flush=True)
        #        continue
        #    try:
        #        if item.retry_limit < 1 :
        #            return
        #        o = item.shopping(item)
        #        if o:
        #            return
        #        item.retry_limit = item.retry_limit - 1
        #        #重试计数
        #        item.retry_count = item.retry_count + 1
        #    except BaseException as be:
        #        #be.with_traceback()
        #        continue
        #pass
        while item.retry_limit > 0:
            time.sleep(item.gap)
            # 当前时间
            cur_time = time.time()
            if cur_time < item.order_time_st:
                print('\r'+' 抢购时间：', item.order_time, '剩余时间：',
                        round(item.order_time_st - cur_time, 2), '秒...', end='', flush=True)
                continue
            else:
                print("执行抢购，第", item.retry_count, "次重试")
                try:
                    item.shopping()
                    item.retry_limit = item.retry_limit - 1
                    # 重试计数
                    item.retry_count += 1
                except BaseException as be:
                    be.with_traceback()
                    continue
                pass
    def shopping(self):
        print("抢购商品：",self.goods_name)
        # 获取商品id，从url的/开始位置截取到.位置
        self.goods_id = self.goods_url[self.goods_url.rindex('/') + 1:self.goods_url.rindex('.')]
        JD.headers['referer'] = self.goods_url
        # url格式化，把商品id填入buy_url
        buy_url = self.buy_url.format(self.goods_id)
        print("添加购物车:")
        self.session.get(url=buy_url, headers=JD.headers)
        # 修正购物车商品数量（第二次重试后修正购物车数量）
        # if self.retry_count > 1 :
        #    print('第',self.retry_count,'次重试，抢购商品为：',self.goods_id,'修正购物车商品数量。')
        #    change_num_url = self.change_num.format(self.goods_id)
        #    self.session.get(url=change_num_url, headers=JD.headers)
        change_num_url = self.change_num.format(self.goods_id)
        print("已修正数量：")
        self.session.get(url=change_num_url, headers=JD.headers)
        # get请求，预下单
        print('下单:')
        self.session.get(url=self.pay_url, headers=JD.headers)
        # post请求，提交订单
        print('提交订单：')
        response = self.session.post(url=self.pay_success, headers=JD.headers)
        print('----response.text:', response.text)
        order_id = json.loads(response.text).get('orderId')
        if order_id:
            print('抢购成功订单号:', order_id)


jd = JD()
jd.login()
while 1:
    time.sleep(0.1)
    pass
