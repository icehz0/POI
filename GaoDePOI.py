#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by hu on 2018/1/25.
"""

# -*- coding:utf-8 -*-
import json
import os
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

class GaoDePOI(object):
    def __init__(self,api_key,itemy,loc):
        self.api_key = api_key
        self.itemy = itemy
        self.loc = loc

    def urls(self):

        # api_key = "Vn1ebvMZ1DCw2nj5LSQ738gmOB8AkCce"
        urls = []
        for pages in range(0,25):
            url = 'http://restapi.amap.com/v3/place/polygon?polygon=' + self.loc +'&offset=25&page=' + str(pages) + '&keywords=' + self.itemy + '&output=json&key=' + self.api_key
            urls.append(url)
        return urls

    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            json_obj = urllib2.urlopen(url)
            print json_obj
            data = json.load(json_obj)
            print data
            if(data['status']=='1'):
                print str(data['count'])
                print 'info:ok'
            else:
                print 'info:error'
            try:
                for item in data['pois']:
                    # print '--------'
                    # print item

                    jid = item['id']
                    jname = item["name"]
                    jtype = item["type"]
                    jtypecode = item["typecode"]
                    jtbiz_type = item["biz_type"]
                    jaddress = item["address"]
                    jlocation = item["location"]
                    jtel = item["tel"]
                    jpname = item["pname"]
                    jcityname = item["cityname"]
                    jadname = item["adname"]

                    jlon =str(jlocation).split(',')[0];
                    jlat =str(jlocation).split(',')[1];

                    jtype1 =str(jtype).split(';')[0];
                    jtype2 =str(jtype).split(';')[1];
                    jtype3 =str(jtype).split(';')[2];

                    # js_sel = str(jlat) + '`' + str(jlon)+'`'+jid+'`'+jname+'`'+jaddress+'`'+jtype1+'`'+jtype2+'`'+jtype3+'`'+jtel+'`'+jtypecode+'`'+jcityname
                    # js_sel = (jlat)+"|"+(jlon)+"|"+jid+"|"+jname+"|"+jaddress+"|"+jtype1+"|"+jtype2+"|"+jtype3+"|"+jtel+"|"+jtypecode+"|"+jcityname
                    js_sel = (jlat)+"|"+(jlon)+"|"+jid+"|"+jname+"|"+str(jaddress)+"|"+str(jtypecode)+"|"+jtype1+"|"+jtype2+"|"+jtype3+"|"+str(jtel)+"|"+str(jcityname)
                    # print js_sel
                    json_sel.append(js_sel)
            except:
                print 'error line'
        return json_sel

class LocaDiv(object):
    def __init__(self,loc_all):
        self.loc_all = loc_all

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0,int((lat_ne-lat_sw+0.0001)/0.05)):
            lat_list.append(lat_sw + 0.05 * i)
        lat_list.append(lat_ne)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0,int((lng_ne-lng_sw+0.0001)/0.05)):
            lng_list.append(lng_sw+0.05*i)
        lng_list.append(lng_ne)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0,len(l1)):
            a = str(l1[i])
            for i2 in range(0,len(l2)):
                b = str(l2[i2])
                ab = a+','+b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0,len(l1)-1):
            for i in range(0+(len(l1)+1)*n,len(l2)+(len(l2))*n-1):
                a = ls_com_v[i]
                b = ls_com_v[i+len(l2)+1]
                ab = a+'|'+b
                ls.append(ab)
        return ls

if __name__ == '__main__':
    baidu_api = ''                                   #这里填入你的百度API
    print "开始爬数据，请稍等..."
    start_time = time.time()
    # loc = LocaDiv('22.44550,113.75719,22.86239,114.62854')#深圳
    # loc = LocaDiv('22.134,113.833,22.564,114.516')#香港
    # loc = LocaDiv('22.150550443811,113.7589819,22.617826947954,114.45751186493')#香港youhuibao
    #baidu
    # c ="商户，丽人，生活服务，商务大厦，地产小区，汽车服务，购物，餐饮，宾馆，休闲娱乐，金融，旅游景点，交通设施，教育，医疗，公司企业，美食，酒店，运动健身，教育培训，文化传媒，房地产，政府机构"

    #高德113.80898,22.5505|113.85898,22.6178
    # loc = LocaDiv('113.75898,22.1505,114.45751,22.6178')#香港youhuibao
    loc = LocaDiv('113.80898,22.5505,113.85898,22.6178')#香港youhuibao
    # c ="餐饮服务，道路附属设施，地名地址信息，风景名胜，公共设施，公司企业，购物服务，交通设施服务，金融保险服务，科教文化服务，摩托车服务，汽车服务，汽车维修，汽车销售，商务住宅，生活服务，事件活动，室内设施，体育休闲服务，通行设施，医疗保健服务，住宿服务，政府机构及社会团体"
    c ="餐饮服务"
    n =c.split("，")
    for item in n:
        print item
        cate = item.decode('utf-8')
        locs_to_use = loc.ls_row()
        for loc_to_use in locs_to_use:
            '''
            百度
            Vn1ebvMZ1DCw2nj5LSQ738gmOB8AkCce  刘海谊
            WwMkKI0MYGXv639HQvunrMOHdN8rnK8H  胡
            KWSoddWr4bd1CXh1gLe4GfmIuPKXuDO9  蔡
            NQ4u00oIVst9I6sCYhMI9Tql3ssfF3rk  蔡
            高德
            a4a4d854ef99369328c358aec9f3b393
            25b16059ee7de0d81ac33da58b3c3c05
            3fe76d8ea22c29d700dddb44e5efcdfc
            '''
            api_key = "3fe76d8ea22c29d700dddb44e5efcdfc"

            print loc_to_use

            par = GaoDePOI(api_key,cate,loc_to_use)            #请修改这里的参数
            a = par.baidu_search()
            doc = open('mark\\'+cate+'.txt','a')
            for ax in a:
                doc.write(ax)
                doc.write('\n')
            doc.close

    end_time = time.time()
    print "数据爬取完毕，用时%.2f秒" % (end_time - start_time)