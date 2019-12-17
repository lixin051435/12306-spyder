# -*- coding: UTF-8 -*-
import requests
import city
import json

def getAll(from_station, to_station, train_date):
    # url请求参数
    from_station_code = city.getCityCode(from_station)
    to_station_code = city.getCityCode(to_station)
    if(from_station_code is None):
        print("出发地错误")
        return
    if(to_station_code is None):
        print("目的地错误")
        return

    # http请求头
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=7AC90DF45333875E241835B6AE0F1A7F; _jc_save_wfdc_flag=dc; RAIL_EXPIRATION=1576855779812; RAIL_DEVICEID=rowBbMVXqihFpp7drcajMTF5o9fm9arPtAlDai_SAwsDzU3TSbGgeC9v27L0Zlnbz3BqIA58-6bWPaKYARlgzLkvu8-ZtFzyuIq8AC2qdIeFvtazcfijzvj7r0WC43gFrTQJwJviiE91zkL7hzyOH4OIuFwnbXvq; BIGipServerpool_passport=283968010.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_toDate=2019-12-17; BIGipServerpassport=954728714.50215.0000; BIGipServerotn=1944584458.50210.0000; _jc_save_fromStation=%u91CD%u5E86%2CCQW; _jc_save_toStation=%u6606%u660E%2CKMM; _jc_save_fromDate=2019-12-20',
        'Host': 'kyfw.12306.cn',
        'If-Modified-Since': '0',
        'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E9%87%8D%E5%BA%86,CQW&ts=%E6%98%86%E6%98%8E,KMM&date=2019-12-20&flag=N,N,Y',
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'%(train_date,from_station_code,to_station_code)

    # print(from_station_code,to_station_code)    
    response = requests.get(url, headers=headers)
    # 不能判断response.status_code == 200 有时会不返回数据，但是状态码还是200
    if(response.content):
        response = response.content.decode('utf-8')

        # text包含BOM字符 需要去掉，否则有时报错
        if response.startswith(u'\ufeff'):
            response = response.encode('utf8')[3:].decode('utf8')

        dictInfo = json.loads(response)

        trainList = dictInfo['data']['result']

        # print("车次\t出发站\t到达站 出发时间 到达时间 商务座 一等座 二等座 硬座  硬卧  软卧  无座 ")
        result = []
        for i in trainList:
            list=i.split("|")
            checi=list[3]
            chufa=city.getCityName(list[6])
            mudi=city.getCityName(list[7])
            ftime=list[8]
            dtime=list[9]
            sw=list[32]
            yd=list[31]
            rw=list[23]
            yw=list[26]
            wuzuo=list[28]
            ed=list[30]
            yz=list[29]
            result.append((checi,chufa,mudi,ftime,dtime,sw,yd,ed,yz,yw,rw,wuzuo))
        return result

# print(getAll("北京","石家庄","2019-12-20"))
if __name__ == "__main__":
    from_station = input('请输入始发地:')
    to_station = input('请输入目的地:')
    train_date = input('请输入日期:')

    list = getAll(from_station,to_station,train_date)
    for item in list:
        print(item)