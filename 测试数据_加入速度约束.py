# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 13:55:54 2018

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
           # print n
            stop_time = (leave_time[b][j] - leave_time[b][j]) * rou[s][j]*2
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



######################速度与稳定性二者结合###############################################

def updata_leavetime(leave_time,station_number, banci_number, m, n ):
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
        fun =lambda x : m*(((head2_23 + (500.0/x- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) - 600)**2) + n*(leave_time['banci%s' %(banci_number)][i] + 500.0/x)  
        sp = minimize(fun, 5).x[0]
        v.append(sp)   
        head2_23 =  (head2_23 + (500.0/sp- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) 
        leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i+1,'banci%s' %(banci_number-1)] + head2_23 
        #leave_time.loc[i + 1,'banci%s' %(banci_number)] = leave_time.loc[i,'banci%s' %(banci_number)] + head2_23* rou.loc[i+1,t1]*2/60.0 + 500/sp

    return leave_time,v
    
leave_time_speed = leave_time.copy()
#leave_time_speed为按照期望速度调整好之后的
for i in range(3,13):
    leave_time_speed = updata_leavetime(leave_time_speed, 10, i, 1, 5)[0] 

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



######################速度与稳定性二者结合###############################################



def updata_leavetime1(leave_time,station_number, banci_number,m,n):
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
        fun =lambda x : m*(((head2_23 + (500.0/x- 500.0/speed.loc[i, s])- rou.loc[i+1, t]*2*(leave_time['banci%s' %(banci_number-1)][i+1] -leave_time['banci%s' %(banci_number-2)][i+1])/60.0)/(1- rou.loc[i+1, t1]*2/60.0) - 600)**2) + n*(leave_time['banci%s' %(banci_number)][i] + 500.0/x)
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

for i in range(3,13):
    leave_time_speed1 = updata_leavetime1(leave_time_speed1, 10, i, 1,1)[0]  

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
    leave_time_speed1 = updata_leavetime1(leave_time_speed1, 10, i,1,1)[0]     
    speed_hope1[i] = updata_leavetime1(leave_time_speed1, 10, i,1,1)[1]





