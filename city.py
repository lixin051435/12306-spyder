# -*- coding: UTF-8 -*-

citys = None
def createCityDict():
    import requests
    import re
    global citys
    if(citys is None):
        requests.packages.urllib3.disable_warnings()
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'
        r = requests.get(url,verify=False)		   #提取网页信息，不判断证书
        pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'  #正则表达式提取中文以及大写英文字母
        result = re.findall(pattern,r.text)        
        citys = dict(result)  
                   
    return citys

# 根据城市代码，返回城市名称
def getCityName(code):
    station = createCityDict()
    for city_name,city_code in station.items():
        if(city_code == code):
            return city_name
    return None

# 根据城市名称，返回12306城市代码
def getCityCode(name):
    station = createCityDict()
    for city_name,city_code in station.items():
        if(city_name == name):
            return city_code
    return None
