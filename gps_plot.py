# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 11:19:04 2017

@author: Liu-pc
"""
import pandas as pd
data = pd.read_excel('C:\Users\Liu-pc\Desktop\\gps1.xlsx',encoding = 'gbk')
data[u'进站时间'] = pd.to_datetime(data[u'进站时间'])



def sort_all_banci(data_gps, fangxiang):
    #把每一个方向的每一天的班次筛选出来，排序
    data1 = data.groupby(u'运行方向')
    data1 = dict(list(data1))
    data1_0 = data1[fangxiang].sort_values(by = [u'车辆编号',u'进站时间',u'站点序号'])
    #data1_0[data1_0[u'站点序号'] == 1][u'进站时间']
    banci = data1_0[data1_0[u'站点序号'] == 1]
    banci = banci.sort_values(by = u'进站时间')
    banci['day'] = map(lambda x:x.day,banci[u'进站时间']) #哪一天的数据
    diff_day = pd.unique(banci['day'])  #不同的天
    ###把每一天的班次排序，4号的1-64班，5号的1-64班
    l = []
    for j in range(len(diff_day)):
        guodu = len(banci[banci['day'] == diff_day[j]])
        print guodu
        l.extend(range(guodu))
    banci['banci_value'] = l
    ##根据'站点序号',u'进站时间'把班次号匹配进原始数据
    banci = banci[[u'站点序号',u'进站时间','banci_value']] 
    banci_result = pd.merge(data1_0, banci, on = [u'站点序号',u'进站时间'],how = 'outer')
    a = banci_result.fillna(method = 'ffill')  
    a['day'] = map(lambda x:x.day,a[u'进站时间'])
    a = a.sort_values(by = ['day','banci_value'])
    return a

a1 = sort_all_banci(data, 1)
a1.index = range(len(a1.index))
#a_tst = a1[(a1[u'车辆编号'] == 20417)&(a1['day'] == 10)]
a_tst = a1[(a1['day'] == 6)&(a1['banci_value']>10) & (a1['banci_value']<41)]
########绘图
'''
import matplotlib as plt
plot(a1[a1['day'] == 4][u'进站时间'][0:23],a1[u'站点序号'][0:23], color='b', linestyle='--', marker='o', label='y1 data')
plot(a1[a1['day'] == 4][u'进站时间'][24:47],a1[u'站点序号'][24:47], color='r', linestyle='-', label='y2 data') 
plot(a1[a1['day'] == 4][u'进站时间'][48:71],a1[u'站点序号'][48:71], color='b', linestyle='--', marker='o', label='y1 data')
plot(a1[a1['day'] == 4][u'进站时间'][72:95],a1[u'站点序号'][72:95], color='r', linestyle='-', label='y2 data') 
plot(a1[a1['day'] == 4][u'进站时间'][96:119],a1[u'站点序号'][96:119], color='b', linestyle='--', marker='o', label='y1 data')
plot(a1[a1['day'] == 4][u'进站时间'][120:143],a1[u'站点序号'][120:143], color='r', linestyle='-', label='y2 data')
plot(m[6])
l = range(23,500,24)
l1 = range(0,500, 24)
'''
#####哪班车缺少哪个站点
def add(data, banci_list, station_number):
    # 原始数据，哪些班次（list），站点个数int数字
    a = range(1,station_number+1) #站点编号
    dic = {}
    for i in range(len(banci_list)):
        s = data[data['banci_value'] == banci_list[i]][u'站点序号']
        s = list(s)

        if len(s) != 16:
            n = list(set(a)-set(s))
            ##n为少了某一站的编号
            dic[banci_list[i]] = n
    return dic
add(a_tst, list(a_tst['banci_value']),16)

#a_tst.loc[5126]={u'站点序号':3,'banci_value':19,'day':6}
##########################################
def find_gap(data):
    #get all gap time
    n = []
    l = []
    dt = pd.DataFrame()
   #b = list(pd.unique(data[data[u'站点序号'] ==1][u'banci_value']))
    n = list(data[data[u'站点序号'] ==1][u'进站时间'])
    for i in range(len(n)-1):
        l.append(n[i+1]-n[i])
    dt['gap'] = l
    return dt
a_gap = find_gap(a_tst)
ba = list(pd.unique(a_tst[a_tst[u'站点序号'] ==1][u'banci_value']))
ba.pop()
a_gap['banc'] = ba
########################################
def get_all_head(data, station_list):
    #get all station head 
    dic = {}
    n = []
    l = []
    for i in range(len(station_list)):
        n = list(data[data[u'站点序号'] == station_list[i]][u'进站时间'])
        for j in range(len(n)-1):
            l.append(n[j+1]-n[j])
        dic[station_list[i]] = l
        l = []
    return dic
a_staion_head = get_all_head(a_tst, [4,7,11,14])    
a_staion_head = pd.DataFrame(a_staion_head)
a_staion_head['banc'] = ba
############################################

a = pd.merge(a_gap,a_staion_head,on = 'banc')


    

a = dict(list(a_tst.groupby('banci_value')))

a = a_tst[(a_tst['banci_value']>10) & (a_tst['banci_value']<41)]
l1 = pd.DataFrame(a[a[u'站点序号'] == 1][[u'进站时间',u'banci_value']])
l_origin = map(lambda x,y: y-x, l1[u'进站时间'][0:28],l1[u'进站时间'][1:29])
l_origin = map(lambda x: x.seconds, l_origin)

l8 = pd.DataFrame(a[a[u'站点序号'] == 9][u'进站时间'])
l8.index = range(len(l8))
l_8 = map(lambda x,y: y-x, l8[u'进站时间'][0:28],l8[u'进站时间'][1:29])
l_8 = map(lambda x: x.seconds, l_8)
l_8[12] = 35 
print 1
#l_with_banci = pd.DataFrame({'x' :list(l_origin),'y' : list(l_8), 'z' : list(l1['banci_value'])[1:29]})
b1 = list(l1['banci_value'])[1:29]

'''
import pylab as pl
绘制点图
pl.plot(l_origin, l_8, 'o')
'''

import matplotlib.pyplot as plt  
import numpy as np
'''
#绘制拟合图，以及函数
f1 = np.polyfit(l_origin, l_8, 1)  
p1 = np.poly1d(f1)
yvals = p1(l_origin)

plot1 = plt.plot(l_origin, l_8, 's',label='original values')  
plot2 = plt.plot(l_origin, yvals, 'r',label='polyfit values') 
plt.legend(list(l1['banci_value'])[1:29], loc='upper left')
plt.show() 
'''
#绘制带有班次标签的图

plt.scatter(
    l_origin, l_8, marker='o',)
#plot2 = plt.plot(l_origin, yvals, 'r',label='polyfit values')
for a,b, c in zip(l_origin, l_8, b1):
    plt.text(a, b, '%s' % c, ha='center', va= 'bottom',fontsize=8)
    
    
    









    