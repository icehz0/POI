#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by hu on 2018/1/25.
"""

# -*- coding:utf-8 -*-
import json
import urllib2
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

class BaiDuPOI(object):
    def __init__(self,api_key,itemy,loc):
        self.api_key = api_key
        self.itemy = itemy
        self.loc = loc

    def urls(self):

        # api_key = "Vn1ebvMZ1DCw2nj5LSQ738gmOB8AkCce"
        urls = []
        for pages in range(0,20):
            url = 'http://api.map.baidu.com/place/v2/search?query=' + self.itemy + '&bounds=' + self.loc +'&scope=2&page_size=20&page_num=' + str(pages) + '&output=json&ak=' + self.api_key
            urls.append(url)
        return urls

    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            json_obj = urllib2.urlopen(url)
            data = json.load(json_obj)
            if(data['status']==0):
                print str(data['total'])
                print 'status:ok'
            else:
                print 'status:error'
            try:
                for item in data['results']:
                    jname = item["name"]
                    jlat = item["location"]["lat"]
                    jlng = item["location"]["lng"]
                    jaddress = item["address"]
                    juid = item["uid"]
                    jtag = item["detail_info"]["tag"]
                    jtype = item["detail_info"]["type"]

                    jtag1 =str(jtag).split(';')[0];
                    jtag2 =str(jtag).split(';')[1];
                    js_sel = str(jlat) + '\t\t' + str(jlng)+'\t\t'+juid+'\t\t'+jname+'\t\t'+jaddress+'\t\t'+jtype+'\t\t'+jtag1+'\t\t'+jtag2
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
                ab = a+','+b
                ls.append(ab)
        return ls

if __name__ == '__main__':
    baidu_api = ''                                   #这里填入你的百度API
    print "开始爬数据，请稍等..."
    start_time = time.time()
    # loc = LocaDiv('22.44550,113.75719,22.86239,114.62854')#深圳
    # loc = LocaDiv('22.134,113.833,22.564,114.516')#香港
    loc = LocaDiv('22.150550443811,113.7589819,22.617826947954,114.45751186493')#香港youhuibao
    # c ="商户，丽人，生活服务，商务大厦，地产小区，汽车服务，购物，餐饮，宾馆，休闲娱乐，金融，旅游景点，交通设施，教育，医疗，公司企业，美食，酒店，运动健身，教育培训，文化传媒，房地产，政府机构"
    c ="政府机构"
    n =c.split("，")
    for item in n:
        print item
        cate = item.decode('utf-8')
        locs_to_use = loc.ls_row()
        for loc_to_use in locs_to_use:
            '''
            Vn1ebvMZ1DCw2nj5LSQ738gmOB8AkCce  刘海谊
            WwMkKI0MYGXv639HQvunrMOHdN8rnK8H  胡
            KWSoddWr4bd1CXh1gLe4GfmIuPKXuDO9  蔡
            NQ4u00oIVst9I6sCYhMI9Tql3ssfF3rk  蔡
            '''
            api_key = "KWSoddWr4bd1CXh1gLe4GfmIuPKXuDO9"

            par = BaiDuPOI(api_key,cate,loc_to_use)            #请修改这里的参数
            a = par.baidu_search()
            doc = open('mark\\'+cate+'.txt','a')
            for ax in a:
                doc.write(ax)
                doc.write('\n')
            doc.close
    end_time = time.time()
    print "数据爬取完毕，用时%.2f秒" % (end_time - start_time)