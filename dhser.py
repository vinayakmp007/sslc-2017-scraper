import requests
import exceptions
import traceback
import re
import urllib
import MySQLdb
import random as rdm
import sys

#This program scrapes data from itschool.gov.in

def fun(url,nm):

    respon=requests.get(url,headers={'Host': 'www.results.itschool.gov.in','User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0','Accept':' */*','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate','Referer': 'http://www.results.itschool.gov.in/result_sslc.html?regno='+str(nm)+'&Submit=Submit','DNT': '1','Connection': 'keep-alive'})      #imitates a ubuntu system
    if respon.status_code==404:                    #if server return page not found
        sp="err"
        return sp
    ht=respon.content
    print(ht)                                   #printing can be avoided here
    # print (sp)
    return ht               #no need for bs4


try:
    db=MySQLdb.connect("localhost","","","")  #hostname, username ,password, and database name of the sql server
    cur=db.cursor()
    print ("cursor created")

    for num in range(100001,602612):

        if num>=100001 and num<=150000:
            fl=1;
        elif num>=150001 and num<=200000:
            fl=2;
        elif num>=200001 and num<=250000:
            fl=3;
        elif num>=250001 and num<=300000:
            fl=4;
        elif num>=300001 and num<=350000:
            fl=5;
        elif num>=350001 and num<=400000:
            fl=6;
        elif num>=400001 and num<=450000:
            fl=7;
        elif num>=450001 and num<=500000:
            fl=8;
        elif num>=500001 and num<=550000:
            fl=9;
        elif num>=550001 and num<=600000:
            fl=10;
        elif num>=600001 and num<=602611:
            fl=11;
        url='http://www.results.itschool.gov.in/itScHoolLreSultzzss/itScHoolLreSultzzsszxsslc_'+str(fl)+'/'+str(num)+'.txt?regno='+str(num)
        print(url)
        n=50                                    #no of retries
        while n:
            n=n-1
            try:
                sp=fun(url,num)
                break
            except:
                if n > 0 :
                    print(sys.exc_info()[0]);
                    print("Trying "+str(n)+":")
                    continue;
                else :
                    print("Failed")

        #print("fdfd")
        if sp=="err":                         #check wherher the server returned data
            continue
        elif sp is not None:
            mdict=dict()
            lin=str(sp).splitlines()
            mdict['name']=lin[1]
            mdict['school']=lin[2]
            mdict['sex']=lin[3]
            mdict['cat']=lin[4]
            mdict['caste']=lin[5]
            mdict['firstlan1']=lin[6]
            mdict['firstlan2']=lin[7]
            mdict['english']=lin[8]
            mdict['hindi']=lin[9]
            mdict['socials']=lin[10]
            mdict['physics']=lin[11]
            mdict['chemistry']=lin[12]
            mdict['bilogy']=lin[13]
            mdict['maths']=lin[14]
            mdict['it']=lin[15]
            mdict['el']=lin[16]
            attrs = ', '.join(['%s'] * len(mdict))
            sql = "Insert Into mar (num,%s) Values ("+str(num)+",%s)"
            sql=sql % (', '.join(mdict.keys()), attrs)
            cur.execute(sql,  mdict.values())

            db.commit()

except :
#    print(cur._last_executed)
    print("Unknown Error")
    print(sys.exc_info()[0])
    traceback.print_exc()
    traceback.print_stack()
finally:
    print (num)
