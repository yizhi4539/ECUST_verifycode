#coding:gbk
from Lib import *
from myverify import *
def ana(tup1,tup2):
    temp=0
    for i in range(len(tup1)):
        for j in range(min(len(tup1[i]),len(tup2[i]))):
            temp+=(abs(tup1[i][j]-tup2[i][j]))
    return temp
def ana2(a1,a2):
    res=0
    for i in range(min(len(a1),len(a2))):
        res+=(abs(a1[i]-a2[i]))
    return res
def gen(filepath,percent=5,codenum=4):
    '''param percent:range from 0 to 100
       codenum:the number of aph you the picture showed
    '''
    para1=percent*1.0/100
    para2=1-para1
    B=getImage(filepath,codenumber=codenum)
    code=''
    for h in range(len(B)):
        t=verify(B[h])
        try:
            sumxy=t.scanxy()
            stage=t.ncc(sumxy)
            mark=t.marrkk()
        except:
            continue
        anaresult={}
        te=[]
        for t1 in Point:
            temp1=ana2(mark,Point[t1])
            anaresult[t1]=temp1
        for t in Stage:
            temp=ana(stage,Stage[t])
            anaresult[t]=anaresult[t]*para1+temp*para2#
        te=[]
        back={}
        for i in anaresult:
            back[anaresult[i]]=i
            te.append(anaresult[i])
        ahp=back[min(te)]
        code+=ahp
    return code

