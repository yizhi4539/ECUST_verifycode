#coding:gbk
from GB75 import *
from math import *
class verify():
    def __init__(self,B):
        self.B=B
        self.col=len(B)
        self.row=len(B[0])
        self.sum=0
        for i in range(self.col):
            for j in range(self.row):
                if self.B[i][j]==0:
                    self.sum+=1
    def marrkk(self):
        markrow=range(0,self.row,int(round(self.row/5.0)))
        markcol=range(0,self.col,int(round(self.col/5.0)))
        if len(markrow)==6:
            markrow[-1]=self.row-1
        else:
            markrow.append(self.row-1)
        if len(markcol)==6:
            markcol[-1]=self.col-1
        else:
            markcol.append(self.col-1)
        mark=[]
        for y in markcol:
            for x in markrow:
                mark.append(self.B[y][x])
        return mark
    def scanxy(self):
        segrow=int(round(self.row*1.0/3))
        segcol1=self.col*1.0/5
        segcol2=self.col*1.0/4
        if abs(segcol1-round(segcol1))>abs(segcol2-round(segcol2)):
            segcol=int(round(segcol2))
            flag=0
        else:
            segcol=int(round(segcol1))
            flag=1
        #列分为三段
        ax=[]
        index=1
        indexrow=range(0,self.row,segrow)
        if len(indexrow)==3:
            indexrow.append(self.row)
        elif len(indexrow)==4:
            indexrow[-1]=self.row
        for i in range(3):
            count=0
            for x in range(indexrow[index-1],indexrow[index]):
                for y in range(self.col):
                    if self.B[y][x]==0:
                        count+=1
            ax.append(count)
            index+=1
        #行分为4/5段
        ay=[]
        index=1
        indexcol=range(0,self.col,segcol)
        
        if flag:
            if len(indexcol)==5:
                indexcol.append(self.col)
            elif len(indexcol)==6:
                indexcol[-1]=self.col
            for i in range(5):
                count=0
                for y in range(indexcol[index-1],indexcol[index]):
                    for x in range(self.row):
                        if self.B[y][x]==0:
                            count+=1
                ay.append(count)
                index+=1
        else:
            if len(indexcol)==4:
                indexcol.append(self.col)
            elif len(indexcol)==5:
                indexcol[-1]=self.col
            for i in range(4):
                count=0
                for y in range(indexcol[index-1],indexcol[index]):
                    for x in range(self.row):
                        if self.B[y][x]==0:
                            count+=1
                ay.append(count)
                index+=1
        sumxy=(ax,ay)
        return sumxy
    def ncc(self,sumxy):
        '''the number change to stage'''
        try:
            numx=sumxy[0]
            numy=sumxy[1]
            #列转换
            ax=[]
            for i in numx:
                ax.append(round(i*1.0/self.sum,4))
            #行转换
            ay=[]
            for t in numy:
                ay.append(round(t*1.0/self.sum,4))
            stage=(ax,ay)
            return stage
        except Exception,e:
            print e
            return (0,0)
def getImage(filename,codenumber):
    '''seg:if seg is True,return a three dimension array,or return a two dimension array'''
    im=getBI(filename,codenumber)
    im.resizee()
    imB=im.getB()
    for i in range(10):
        imB=im.ftr(imB)
    #B=im.compensate(imB)
    B=im.ftr(imB,col1=False,col2=True,col3=True)
    B=im.compensate(B)
    imBt=im.reshape(B)
    le=[]
    for i in imBt:
        le.append(len(i))
    if max(le)*1.0/min(le)>2.5:
        #print "****************************"
        Bh=im.ftr(B,col1=False,col2=True,n2=2)
        imBt=im.reshape(Bh)
    return imBt
class chage:
    def __init__(self,char,content):
        self.char=char
        self.c=content
    def ch(self):
        l=len(self.c[0])
        temp=[]
        for i in range(l):
            temp.append([])
        for t in range(len(self.c[0])):
            k=len(self.c[0][t])
            for i in range(k):
                temp[t].append(0)
        for i in range(len(self.c)):
            for j in range(len(self.c[i])):
                for k in range(len(self.c[i][j])):
                    try:
                        temp[j][k]+=self.c[i][j][k]
                    except:
                        pass
        length=len(self.c)
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                temp[i][j]=round(temp[i][j]*1.0/length,4)
        return temp
def change2(a):
    l=len(a[0])
    temp=[]
    for i in range(l):
        temp.append(0)
    length=len(a)
    for j in range(length):
        for i in range(l):
            try:
                temp[i]+=a[j][i]
            except:
                temp[i]+=0
    for i in range(l):
        temp[i]=round(temp[i]*1.0/length,4)
    return temp

    
        
