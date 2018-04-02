# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:24:51 2017

@author: Liu-pc
"""

import pandas as pd
from scipy.optimize import minimize
rou = pd.read_csv('C:\Users\Liu-pc\Desktop\simulation\\rou.csv')
speed = pd.read_csv('C:\Users\Liu-pc\Desktop\simulation\\speed.csv')
leave_time = pd.DataFrame({'stiation':range(1,12)})
'''
TS1_1 = 10   #第一班在第一站的停留时间
leave1_1 =0 + TS1_1
TT1_1_2  = 500.0/speed.loc[1,'speed_1'] # 第一班车在第一二站之间的行程时间

leave1_2 = leave1_1 + TT1_1_2 + 10
'''
#####第一班
leave = [0]
for i in range(10):
    n = int(leave[-1]/500) +1
    n = str('speed_%s') %n
    l = 500.0/speed.loc[i,n] + leave[i] +10
    leave.append(l)
    
leave_time['banci1'] = leave
#####第二班
leave = [600]
for i in range(10):
    n = int(leave[-1]/500) +1
    n = str('speed_%s') %n
    print n
    l = 500.0/speed.loc[i,n] + leave[i] + 10
    leave.append(l)
leave_time['banci2'] = leave
#####第三班
'''
leave = [1200]
for i in range(10):
    n = int(leave[-1]/500) +1
    n1 = str('speed_%s') %n
    s = str('time_%s') %n
    print n
    stop_time = (leave_time['banci2'][i] - leave_time['banci2'][i]) * rou[s][n]*2
    l = 500.0/speed.loc[i,n1] + leave[i] + stop_time
    leave.append(l)
leave_time['banci3'] = leave
'''
#####往后多算四班(第3,4,5,6)班，如果要算更多，请保持足够多的rou列【time_n。。。】
def leave_time_function(n_ban,station, leave_time):
    l = range(1200,8000,600)
    for i in range(n_ban):
        leave = [l[i]]
        for j in range(station-1):
            n = int(leave[-1]/600) + 1
            n1 = str('speed_%s') %n
            s = str('time_%s') %n
            b = str('banci%s') %(i+2)
            b1 = str('banci%s') %(i+1)
           # print n
            stop_time = (leave_time[b][j +1] - leave_time[b1][j +1 ]) * rou[s][j]*2/60
            t = 500.0/speed.loc[j,n1] + leave[j] + stop_time
            #print t
            leave.append(t)
       # print i
        leave_time['banci%s' %(i+3)] = leave
    return leave_time

leave_time = leave_time_function(11,11,leave_time)
  
plt.plot(leave_time['stiation'], leave_time['banci1'], color='y', linestyle='-', label='y2 data')       
plt.plot(leave_time['stiation'], leave_time['banci2'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci3'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci4'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci5'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci6'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci7'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci8'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci9'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci10'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci11'], color='y', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci12'], color='y', linestyle='-', label='y2 data')
#plt.plot(leave_time['stiation'], leave_time['banci13'], color='y', linestyle='-', label='y2 data')
plt.xlabel('station')
plt.ylabel('time(s)')
#savefig('C:\Users\Liu-pc\Desktop\simulation\\origin.png', dpi=200)

################给出期望速度,以及在这个速度下的leave_time
from scipy.optimize import minimize
'''
sqr = lambda p:(p-2)**2 
minimize(sqr, 2)


n = int(leave_time['banci2'][0] /600) + 1
t = str('time_%s') %n
n1 = int(leave_time['banci3'][0] /600) + 1
t1 = str('time_%s') %n1
n1 = int(leave_time['banci2'][0] /600) + 1
s = str('speed_%s') %n1

fun =lambda x : ((600 + (500.0/x- 500.0/speed.loc[0, s])- rou.loc[1, t]*2*(leave_time['banci2'][1] -leave_time['banci1'][1])/60.0)/(1- rou.loc[1, t1]*2/60.0) - 600)**2
sp = minimize(fun, 5).x[0]
#把sp带入可以得到2，3车在第2站的head，之后便可以带入下一次循环
head2_23 =  (600 + (500.0/sp- 500.0/speed.loc[0, s])- rou.loc[1, t]*2*(leave_time['banci2'][1] -leave_time['banci1'][1])/60)/(1- rou.loc[1, t1]*2/60)
#如果按照这个速度可以求出在下一站(2站)的leave_time，更新leave_time表
leave_time.loc[1,'banci3'] = leave_time.loc[1,'banci2'] + head2_23
#计算下一个站的期望速度，首先更新，t，t1，s#####################
n = int(leave_time['banci2'][1] /600) + 1
t = str('time_%s') %n
n1 = int(leave_time['banci3'][1] /600) + 1
t1 = str('time_%s') %n1
n1 = int(leave_time['banci2'][1] /600) + 1
s = str('speed_%s') %n1

fun =lambda x : ((head2_23 + (500.0/x- 500.0/speed.loc[0, s])- rou.loc[1, t]*2*(leave_time['banci2'][1] -leave_time['banci1'][1])/60)/(1- rou.loc[1, t1]*2/60) - 600)**2
sp = minimize(fun, 5).x[0]
'''
def updata_leavetime(leave_time,station_number, banci_number,):
    #总共多少站，计算第几班两个参数
    head2_23 = 600
    v = []
    for i in range(station_number):
        n = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        t = str('time_%s') %n
        n1 = int(leave_time['banci%s' %(banci_number)][i] /600) + 1
        t1 = str('time_%s') %n1
        n1 = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        s = str('speed_%s') %n1
        fun =lambda x : ((head2_23 + (500.0/x- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) - 600)**2 
        sp = minimize(fun, 5).x[0]
        v.append(sp)   
        head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
        leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
        #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60.0 + 500/sp

    return leave_time,v
    
leave_time_speed = leave_time.copy()
#leave_time_speed为按照期望速度调整好之后的
for i in range(3,13):
    leave_time_speed = updata_leavetime(leave_time_speed, 10, i)[0] 
    
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci1'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci2'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci3'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci4'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci5'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci6'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci7'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci8'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci9'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci10'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci11'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci12'], color='b', linestyle='-', label='y2 data')   
#plt.plot(leave_time_speed['stiation'], leave_time_speed['banci13'], color='b', linestyle='-', label='y2 data')   



plt.xlabel('station')
plt.ylabel('time(s)')
#savefig('C:\Users\Liu-pc\Desktop\simulation\\hope.png', dpi=200)

#########原始的行车速度
def leave_time_function_speed(n_ban,station):
    l = range(1200,8000,600)
    v = []
    sped = {}
    for i in range(n_ban):
        leave = [l[i]]
        for j in range(station-1):
            n = int(leave[-1]/600) + 1
            n1 = str('speed_%s') %n
            s = str('time_%s') %n
            b = str('banci%s') %(i+2)
            print n
            stop_time = (leave_time[b][j] - leave_time[b][j]) * rou[s][j]*2
            t = 500.0/speed.loc[j,n1] + leave[j] + stop_time
            leave.append(t)
            v.append(speed.loc[j,n1])
        leave_time['banci%s' %(i+3)] = leave
        sped[i +3] = v
        v = []
    return sped   
 
speed_origin = leave_time_function_speed(10,11)    
##########期望的行车速度
speed_hope = {}
for i in range(3,13):
    leave_time_speed = updata_leavetime(leave_time_speed, 10, i)[0]     
    speed_hope[i] = updata_leavetime(leave_time_speed, 10, i)[1]
###speed_hope为期望速度
#    speed_origin为原始速度
    
    
'''
def updata_leavetime(leave_time,station_number, banci_number,):
    #总共多少站，计算第几班两个参数
    head2_23 = 600
    v = []
    for i in range(station_number):
        n = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        t = str('time_%s') %n
        n1 = int(leave_time['banci%s' %(banci_number)][i] /600) + 1
        t1 = str('time_%s') %n1
        n1 = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        s = str('speed_%s') %n1
        fun =lambda x : ((head2_23 + (500.0/x- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) - 600)**2 
        sp = minimize(fun, 5).x[0]
        #v.append(sp)
        if i <station_number -1:
            if sp > speed.loc[i, s]:
                sp = speed.loc[i, s]
                head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
                print head2_23, s, i+1
                leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
                #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60 + 500/sp
       
            elif sp <speed.loc[i, s]:
                sp = sp
                head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
                #print head2_23
                leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
                #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60 + 500/sp
        else:
            sp = 3
            head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
            leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
            #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60 + 500/sp

        v.append(sp)
    return leave_time,v
    
leave_time_speed = leave_time.copy()
#leave_time_speed为按照期望速度调整好之后的
for i in range(3,14):
    leave_time_speed = updata_leavetime(leave_time_speed, 10, i)[0]     
'''   
    
def updata_leavetime(leave_time,station_number, banci_number,):
    #总共多少站，计算第几班两个参数
    head2_23 = 600
    v = []
    for i in range(station_number):
        n = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        t = str('time_%s') %n
        n1 = int(leave_time['banci%s' %(banci_number)][i] /600) + 1
        t1 = str('time_%s') %n1
        n1 = int(leave_time['banci%s' %(banci_number-1)][i] /600) + 1 
        s = str('speed_%s') %n1
        n1 = int(leave_time['banci%s' %(banci_number)][i] /600) + 1 
        s1 = str('speed_%s') %n1
        fun =lambda x : ((head2_23 + (500.0/x- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) - 600)**2 
        sp = minimize(fun, 5).x[0]
        #v.append(sp)
        if sp > speed.loc[i, s1]:
            sp = speed.loc[i, s1]
            head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
            #print head2_23, s, i+1
            leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
            #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60 + 500/sp
       
        elif sp <speed.loc[i, s1]:
            sp = sp
            head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
            print head2_23
            leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
            #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60 + 500/sp
        v.append(sp)
    return leave_time,v
    
leave_time_speed1 = leave_time.copy()
#leave_time_speed为按照期望速度调整好之后的

for i in range(3,14):
    leave_time_speed1 = updata_leavetime(leave_time_speed1, 10, i)[0]  

plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci1'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci2'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci3'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci4'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci5'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci6'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci7'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci8'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci9'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci10'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci11'], color='b', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci12'], color='b', linestyle='-', label='y2 data')   
#plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci13'], color='b', linestyle='-', label='y2 data')   
plt.xlabel('station')
plt.ylabel('time(s)')
#savefig('C:\Users\Liu-pc\Desktop\simulation\\limit_hope.png', dpi=200)


speed_hope1 = {}
for i in range(3,13):
    leave_time_speed1 = updata_leavetime(leave_time_speed1, 10, i)[0]     
    speed_hope1[i] = updata_leavetime(leave_time_speed1, 10, i)[1]








###################计算每一班行程时间


def travel_time(data, station_number,banci_st):
    #数据， 一共多少站， 第多少班
    return data[banci_st][station_number-1 +5] - data[banci_st][0 + 5]

origin_traveltime = []
for i in leave_time.axes[1][1:13]:
    l = travel_time(leave_time,6,i)
    origin_traveltime.append(l)

hope_traveltime = []
for i in leave_time_speed.axes[1][1:13]:
    l = travel_time(leave_time_speed,6,i)
    hope_traveltime.append(l)


limit_hope_traveltime = []
for i in leave_time_speed1.axes[1][1:13]:
    l = travel_time(leave_time_speed1,6,i)
    limit_hope_traveltime.append(l)


pd.mean(map(lambda x,y: (x-y)/y, limit_hope_traveltime,origin_traveltime))
#平均增加损失时间39.48%
#如果用hope的非但不损失还可以增加9.8%的速度

#下面计算车头时距的稳定性增加多少##########

#1车头时距数值
def head1(data):
    dic = pd.DataFrame()
    h = []
    for j in range(11):
        n = j+1
        b = 'banci%i' %(n)
        b1 = 'banci%i' %(n+1)
        for k in range(11):
            r = data[b1][k] - data[b][k]
            h.append(r)
        dic[b] = h
        h = []
    return dic

a = head1(leave_time)
a_hope=  head1(leave_time_speed)
a_limit =  head1(leave_time_speed1)

del a['banci12']
del a_hope['banci12']
del a_limit['banci12']

#与600 的平均绝对误差是多少
def abs_cha(data):
    dic = pd.DataFrame()
    h = []
    for j in range(12):
        n = j+1
        b = 'banci%i' %(n)
        b1 = 'banci%i' %(n+1)
        for k in range(11):
            r = abs(data[b1][k] - data[b][k] - 600)
            h.append(r)
        dic[b] = h
        h = []
    return dic
a_cha = abs_cha(leave_time)
a_hope_cha=  abs_cha(leave_time_speed)
a_limit_cha =  abs_cha(leave_time_speed1)

del a_cha['banci12']
del a_hope_cha['banci12']
del a_limit_cha['banci12']


'''
a_mean_abs = []
for i in a_cha.keys():
    a_mean_abs.append(mean(a_cha[i]))
    
    
a_hope_mean_abs = []
for i in a_hope_cha.keys():
    a_hope_mean_abs.append(mean(a_hope_cha[i]))
    
a_limit_mean_abs = []
for i in a_limit_cha.keys():
    a_limit_mean_abs.append(mean(a_limit_cha[i]))
    
mean(a_mean_abs)
mean(a_limit_mean_abs)
#稳定性提高22%
#如果用hope的可以提高89.8%的稳定性



#方差
a = mean(hope_traveltime)
a1 = 0
for i in hope_traveltime:
    a1 = a1 + (i-a)**2

sqrt(a1)/12
'''

class1 = []
for i in a.keys():
    class1.extend(list(a[i]))
    
class2 = []
for i in a_hope.keys():
    class2.extend(list(a_hope[i])) 
    
class3 = []
for i in a_limit.keys():
    class3.extend(list(a_limit[i]))
    
    
#求均值和标准差    
import numpy as np
class1 = np.array(class1)
class2 = np.array(class2)
class3 = np.array(class3)

np.std(class1)
np.mean(class1)
np.std(class2)
np.mean(class2)
np.std(class3)
np.mean(class3)
###########################################################################
a_head = a_cha.mean().mean()
a_head_hope = a_hope_cha.mean().mean()
a_head_limit = a_limit_cha.mean().mean()
######################车头时距图#################################################
a_mean_var = pd.DataFrame({u'均值':[612.4,607.6,690.4], u'标准差':[182.4,40.8,129.4] })
'''
del a['banci12']
del a_hope['banci12']
del a_limit['banci12']
'''
import matplotlib.pyplot as plt  
import numpy as np  
import matplotlib as mpl  
from matplotlib.font_manager import FontProperties as FP

mpl.rcParams['font.family'] = 'sans-serif'  
mpl.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'  #//中文除外的设置成New Roman，中文设置成宋体  

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False



fig = plt.figure()
cfp = FP('NSimSun', size=12)
efp = FP('Times New Roman', size=12)

ax1 =fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

ax1.plot(a, color = 'black')
ax1.set_ylim([200,1200])
ax1.set_yticklabels(['250','250', '500', '750', '1 000'],fontproperties= efp)

ax1.set_xticks(range(0,12))
ax1.set_xticklabels(range(1,12))
ax1.set_xlabel(u'站点', fontsize=13.5)
ax1.set_ylabel(u'车头时距/s', fontsize=13.5)
ax1.legend(loc = 'beat')
ax1.set_title(u'场景1', fontsize=13.5)

ax2.plot(a_hope,color = 'black')
ax2.set_ylim([200,1200])
ax2.set_xticks(range(0,12))
ax2.set_xticklabels(range(1,12))
ax2.set_xlabel(u'站点', fontsize=13.5)
ax2.set_ylabel(u'车头时距/s', fontsize=13.5)
ax2.set_title(u'场景2', fontsize=13.5)

ax3.plot(a_limit, color = 'black')
ax3.set_ylim([200,1200])
ax3.set_xticks(range(0,12))
ax3.set_xticklabels(range(1,12))
ax3.set_xlabel(u'站点', fontsize=13.5)
ax3.set_ylabel(u'车头时距/s', fontsize=13.5)
ax3.set_title(u'场景3', fontsize=13.5)


x = np.arange(1,4)
y1 =  np.array(a_mean_var[u'均值'])
y2 =  np.array(a_mean_var[u'标准差'])
bar_width = 0.35
#ax4.hist(x,y1,bins=7)
ax4.set_xlim([0,4])
ax4.set_ylim([0, 800])
ax4.set_ylabel(u'均值/s', fontsize=13.5)
ax4.set_title(u'均值以及标准差 ', fontsize=13.5)
plt.bar(x, y1, bar_width, color='black', label=u'均值')
ax4.set_xticklabels([' ',u'场景1',u'场景2',u'场景3',' '], fontsize=13.5)
plt.legend( loc='upper center',bbox_to_anchor=((0.25, -0.18)), fontsize=11)

ax5 = ax4.twinx()
ax5.set_ylim([0, 200])
ax5.set_xlim([0,4])
ax5.set_ylabel(u'标准差/s', fontsize=13.5)
plt.bar(x+ bar_width, y2, bar_width, color='grey', label=u'标准差')
#plt.bar(x+ bar_width, y2, bar_width, color='#ED1C24', label='var')

#plt.bar(label='var')
plt.legend(loc='upper center',bbox_to_anchor=((0.75, -0.18)), fontsize=11)

plt.subplots_adjust(wspace = 0.42,hspace = 0.7)
savefig('C:\Users\Liu-pc\Desktop\simulation\\mean_std.tif', dpi=700)

################将运行状态图绘制在一个图里###############################################
fig1 = plt.figure()

ax1 =fig1.add_subplot(2,2,1)

#ax4 = fig1.add_subplot(2,2,4)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
ax1.set_xticks(range(1,12))
ax1.set_ylim([0,10000])
ax1.set_yticklabels(['0','2 500', '5 000', '7 500', '10 000'])

ax1.set_title(u'场景1', fontsize=13.5)
plt.plot(leave_time['stiation'], leave_time['banci1'], color='black', linestyle='-', label='y2 data')       
plt.plot(leave_time['stiation'], leave_time['banci2'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci3'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci4'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci5'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci6'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci7'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci8'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci9'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci10'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci11'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time['stiation'], leave_time['banci12'], color='black', linestyle='-', label='y2 data')
#plt.plot(leave_time['stiation'], leave_time['banci13'], color='y', linestyle='-', label='y2 data')
plt.xlabel(u'站点', fontsize=13.5)
plt.ylabel(u'时间/s', fontsize=13.5)

ax2 = fig1.add_subplot(2,2,2)
ax2.set_xticks(range(1,12))
ax2.set_ylim([0,10000])
ax2.set_yticklabels(['0','2 500', '5 000', '7 500', '10 000'])
ax2.set_title(u'场景2', fontsize=13.5)
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci1'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci2'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci3'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci4'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci5'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci6'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci7'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci8'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci9'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci10'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci11'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed['stiation'], leave_time_speed['banci12'], color='black', linestyle='-', label='y2 data')   
#plt.plot(leave_time_speed['stiation'], leave_time_speed['banci13'], color='b', linestyle='-', label='y2 data')   
plt.xlabel(u'站点', fontsize=13.5)
plt.ylabel(u'时间/s', fontsize=13.5)

ax3 = fig1.add_subplot(2,2,3)
ax3.set_xticks(range(1,12))
ax3.set_ylim([0,10000])
ax3.set_yticklabels(['0','2 500', '5 000', '7 500', '10 000'])
ax3.set_title(u'场景3', fontsize=13.5)
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci1'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci2'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci3'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci4'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci5'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci6'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci7'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci8'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci9'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci10'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci11'], color='black', linestyle='-', label='y2 data')
plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci12'], color='black', linestyle='-', label='y2 data')   
#plt.plot(leave_time_speed1['stiation'], leave_time_speed1['banci13'], color='b', linestyle='-', label='y2 data')   
plt.xlabel(u'站点', fontsize=13.5)
plt.ylabel(u'时间/s', fontsize=13.5)

plt.subplots_adjust(wspace = 0.48,hspace = 0.7)
savefig('C:\Users\Liu-pc\Desktop\simulation\\zhuangtai.tif',dpi=700)


###################方式1,2,3 在每一站的车头时距平均绝对误差##############
#use a_cha a_hope_cha  a_limit_cha
'''
del a_cha['banci12']
del a_hope_cha['banci12']
del a_limit_cha['banci12']
'''
a_abs_Cha = pd.DataFrame({'class1':list(a_cha.T.mean()), 'class2':list(a_hope_cha.T.mean()), 'class3':list(a_limit_cha.T.mean())})
a_abs_Cha = a_abs_Cha[['class1','class2','class3']]
a_abs_Cha.index = range(1,12)

#a_abs_Cha.plot(xticks= range(1,12))

l1, = plt.plot(a_abs_Cha.index,a_abs_Cha['class1'], '--', color = 'black')
l2, = plt.plot(a_abs_Cha.index,a_abs_Cha['class2'], ':',color = 'black')
l3, = plt.plot(a_abs_Cha.index,a_abs_Cha['class3'], '-',color = 'black')
plt.legend((l1, l2,l3),(u'场景1',u'场景2',u'场景3'), loc = 'upper left',  fontsize=13.5)
plt.xticks(range(1,12),  fontsize=13.5)
plt.yticks(range(0,250,50),  fontsize=13.5)
plt.xlabel(u'站点',  fontsize=14.8)
plt.ylabel(u'车头时距绝对误差/s', fontsize=15.5)
#plt.figure(figsize=(3,2.7559055)) 
savefig('C:\Users\Liu-pc\Desktop\simulation\\3class_abs_head_.tif', dpi=500)


###########################累计总行程时间###########################################
del leave_time['banci13']
del leave_time_speed['banci13']
del leave_time_speed1['banci13']
 
    
def travel_time(data, station_gap):
    l = 0
    for i in data.axes[1]:
        l=l + data[i][station_gap +1 ] - data[i][station_gap]
    return l/len(data.axes[1])


sum_travel_time = []
avg = 0
for i in range(10):
    avg = avg + travel_time(leave_time, i)
    sum_travel_time.append(avg)
    
sum_travel_time_Speed = []
avg = 0
for i in range(10):
    avg = avg + travel_time(leave_time_speed, i)
    sum_travel_time_Speed.append(avg)   
    
    
sum_travel_time_Speed1 = []
avg = 0
for i in range(10):
    avg = avg + travel_time(leave_time_speed1, i)
    sum_travel_time_Speed1.append(avg)   



sum_tt = pd.DataFrame({'class1': sum_travel_time,'class2':sum_travel_time_Speed,'class3':sum_travel_time_Speed1})
sum_tt.index = range(1,11)


#sum_tt.plot()

l1, = plt.plot(sum_tt.index,sum_tt['class1'], 'r--')
l2, = plt.plot(sum_tt.index,sum_tt['class2'], ':')
l3, = plt.plot(sum_tt.index,sum_tt['class3'], '-.')
plt.legend((l1, l2,l3),('class1','class2','class3'), loc = 'upper left')
plt.xticks(range(1,11))
plt.xlabel('station_gap')
plt.ylabel('travel_time(s)')
savefig('C:\\Users\\Liu-pc\\Desktop\simulation\\sum_traveltime_.png', dpi=200)


##########################速度分布图##############################################

speed_origin = pd.DataFrame(speed_origin)
speed_hope = pd.DataFrame(speed_hope)
speed_hope1 = pd.DataFrame(speed_hope1)



'''
fig2 = plt.figure()
#ax1 =fig2.add_subplot(3,3,1)
for i in range(1,10):   
    speed_tst = pd.DataFrame({'class1':list(speed_origin[i+3]), 'class2':list(speed_hope[i+3]), 'class3':list(speed_hope1[i+3])})
    speed_tst.index = range(1,11)
    ax = fig2.add_subplot(3,3,i) 
   
    l1, = ax.plot(speed_tst.index,speed_tst['class1'], '--', color  = 'black')
    l2,= ax.plot(speed_tst.index,speed_tst['class2'], ':',color  = 'black')
    l3, = ax.plot(speed_tst.index,speed_tst['class3'], '-', color  = 'black')
    plt.legend((l1, l2,l3),(u'场景1',u'场景2',u'场景3'), loc = 'upper center',prop={'size':3.5} ,ncol=3)

    ax.set_xlabel(u'站间编号')
    ax.set_ylabel(u'速度/s')
    ax.set_xticks(range(1,11))
    #ax.set_yticks(range(1,7,2))
    ax.set_ylim([1,7])
    ax.set_title(u'班次%s' %(i+3))
plt.subplots_adjust(wspace = 0.7,hspace = 1.3)

'''


fig2 = plt.figure()
#ax1 =fig2.add_subplot(3,3,1)
n = 1
for i in [0,1,6,7]:   
    speed_tst = pd.DataFrame({'class1':list(speed_origin[i+3]), 'class2':list(speed_hope[i+3]), 'class3':list(speed_hope1[i+3])})
    speed_tst.index = range(1,11)
    ax = fig2.add_subplot(2,2,n) 
   
    l1, = ax.plot(speed_tst.index,speed_tst['class1'], '--', color  = 'black')
    l2,= ax.plot(speed_tst.index,speed_tst['class2'], ':',color  = 'black')
    l3, = ax.plot(speed_tst.index,speed_tst['class3'], '-', color  = 'black')
    plt.legend((l1, l2,l3),(u'场景1',u'场景2',u'场景3'), loc = 'upper center',prop={'size':9} ,ncol=2)

    ax.set_xlabel(u'站间编号',  fontsize=13.5)
    ax.set_ylabel(u'速度/s',  fontsize=13.5)
    plt.xticks(range(1,11),  fontsize=13.5)
    #ax.set_yticks(range(1,7,2))
    plt.yticks(range(0,9,2),  fontsize=13.5)
    ax.set_title(u'班次%s' %(n+3),  fontsize=15.5)
    n = n+1
plt.subplots_adjust(wspace = 0.42,hspace = 0.8)
savefig('C:\\Users\\Liu-pc\\Desktop\simulation\\speed_distribute_.tif', dpi=700)


'''
for i in speed_origin.axes[1]:
    plt.scatter(speed_origin.index, speed_origin[i],color = 'black')

for i in speed_hope.axes[1]:
    plt.scatter(speed_hope.index, speed_hope[i],color = 'blue')

for i in speed_hope1.axes[1]:
    plt.scatter(speed_hope1.index, speed_hope1[i],color = 'red')
   
    
    
fig2 = plt.figure()
ax1 =fig2.add_subplot(2,2,1)
    
for i in speed_origin.axes[1]:
    plt.scatter(speed_origin.index, speed_origin[i],color = 'black') 
    
'''    
#############################乘客平均等待时间#############################    
    
def wait_time(data):
    return np.mean(data)*(1 + np.var(data)/(np.mean(data))**2)/2


w1 = []
for i in range(11):
    w1.append(wait_time(a.T[i]))


w2 = []
for i in range(11):
    w2.append(wait_time(a_hope.T[i]))

w3 = []
for i in range(11):
    w3.append(wait_time(a_limit.T[i]))


wait_t = pd.DataFrame({'class1':w1, 'class2':w2, 'class3':w3})
wait_t.index = range(1,12)

l1, = plt.plot(wait_t.index,wait_t['class1'], '--', color  = 'black')
l2,= plt.plot(wait_t.index,wait_t['class2'], ':',color  = 'black')
l3, = plt.plot(wait_t.index,wait_t['class3'], '-',color  = 'black')
plt.legend((l1, l2,l3),(u'场景1',u'场景2',u'场景3'), loc = 'upper left' , fontsize = 10.5)
plt.xticks(range(1,12),  fontsize=15.5)
plt.xlabel(u'站点', fontsize = 15.5)
plt.ylabel(u'平均等待时间/s',  fontsize=15.5)
plt.yticks(range(0,500,50),  fontsize=15.5)

#plt.ylim([0,450])


savefig('C:\\Users\\Liu-pc\\Desktop\simulation\\wait_time1_.tif', dpi=500)


#####################################

from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(400, 800, 1)
Y = np.arange(20, 180, 1)
X, Y = np.meshgrid(X, Y)
R = X*(1+ (Y/X)**2)/2
Z = R
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

savefig('C:\\Users\\Liu-pc\\Desktop\simulation\\functin_.gif', dpi=350)






a_limit.T.to_csv('C:\Users\Liu-pc\Desktop\\fig\\head3.csv')








