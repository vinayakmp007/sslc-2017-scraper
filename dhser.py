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
    db=MySQLdb.connect("localhost","","","")  # enter hostname, username ,password, and database name of the sql server
    cur=db.cursor()
    print ("cursor created")

    for num in range(100001,602612):
        url='http://www.results.itschool.gov.in/itScHoolLreSultzzss/itScHoolLreSultzzsszxsslc_1/'+str(num)+'.txt?regno='+str(num)
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
    print(cur._last_executed)
    print("Unknown Error")
    print(sys.exc_info()[0])
    traceback.print_exc()
    traceback.print_stack()
finally:
    print (num)
