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


class JD:
    headers = {
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    def __init__(self):
        # 配置项 只要填这5个 1.cookie 2.url 3.秒杀时间 4.秒杀总次数限制 5.秒杀请求间隙
        self.thor = ''
        #影驰黑将5499
        #self.goods_url = 'https://item.jd.com/100015325218.html'
        #self.order_time = '2020-11-27 10:00:00.0'
        #盈通6800xt
        #self.goods_url = 'https://item.jd.com/100016642488.html'
        #self.order_time = '2020-11-27 10:00:00.0'
        #蓝宝石6800xt
        #self.goods_url = 'https://item.jd.com/100016553676.html'
        #self.order_time = '2020-12-01 15:00:00.0'
        #技嘉6800xt
        #self.goods_url = 'https://item.jd.com/100009514841.html'
        #self.order_time = '2020-12-01 15:00:00.0'
        #次数设定
        self.retry_limit = 1
        #间隔设定
        self.gap = 0.2

        self.index = 'https://www.jd.com/'
        #用户信息获取地址
        self.user_url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?&callback=jsonpUserinfo&_=' + \
            str(int(time.time() * 1000)) 
        #加购物车
        self.buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'   
        #修改购物车商品数量为1
        self.change_num = 'https://cart.jd.com/changeNum.action?pid={}&pcount=1&ptype=1'
        #下单
        self.pay_url = 'https://cart.jd.com/gotoOrder.action'  
        #订单提交
        self.pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'
        self.goods_id = ''  
        self.session = requests.session()

		    #重试计数
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
        print('账号：', user_info.get('nickName'))
        if user_info.get('nickName'):
            while self.retry_limit > 0:
                time.sleep(self.gap)
                #当前时间
                cur_time = time.time()
                if cur_time < self.order_time_st:
                    print('\r'+' 抢购时间：',self.order_time, '剩余时间：',round(self.order_time_st - cur_time,2),'秒...',end='', flush=True)
                    continue
                else:
                  print("执行抢购，第",self.retry_count,"次重试")
                  try:
                      self.shopping()
                      self.retry_limit = self.retry_limit - 1
                      #重试计数
                      self.retry_count += 1
                  except BaseException as be:
                      be.with_traceback()
                      continue
                  pass

    def shopping(self):
        #获取商品id，从url的/开始位置截取到.位置
        self.goods_id = self.goods_url[
            self.goods_url.rindex('/') + 1:self.goods_url.rindex('.')]
        JD.headers['referer'] = self.goods_url
        # url格式化，把商品id填入buy_url
        buy_url = self.buy_url.format(self.goods_id)
        print("添加购物车:")
        self.session.get(url=buy_url, headers=JD.headers)  
		    #修正购物车商品数量（第二次重试后修正购物车数量）
        if self.retry_count > 1 :
            print('第',self.retry_count,'次重试，抢购商品为：',self.goods_id,'修正购物车商品数量。')
            change_num_url = self.change_num.format(self.goods_id)
            self.session.get(url=change_num_url, headers=JD.headers)
        #get请求，预下单
        print('下单:')
        self.session.get(url=self.pay_url, headers=JD.headers)
        #post请求，提交订单
        print('提交：')
        response = self.session.post(
            url=self.pay_success, headers=JD.headers)     
        print('----response.text:',response.text)
        order_id = json.loads(response.text).get('orderId')
        if order_id:
            print('抢购成功订单号:', order_id)

jd = JD()
jd.login()	

  
