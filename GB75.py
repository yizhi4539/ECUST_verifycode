#!python2
#coding:gbk
import os
from PIL import Image
class getBI(Image.Image):
    def __init__(self,name,number):
        Image.Image.__init__(self)
        self.imagefile=Image.open(name).convert("L")
        self.box=self.imagefile.getbbox()
        self.number=number
        self.size=self.box[-2:]
        self.x=self.size[0]
        self.y=self.size[1]
        self.colorlist=list(self.imagefile.getdata())
    def resizee(self):
        '''deform the original one dimension array into two dimension array'''
        self.data=[]
        for i in range(self.y):
            self.data.append([])
        n=0
        for y in range(self.y):
            for x in range(self.x):
                self.data[y].append(self.colorlist[n])
                n+=1
    def getB(self,threshold=170):
        '''get the two dimension binary array'''
        self.B=[]
        for t in range(self.y):
            self.B.append([])
        for y in range(self.y):
            for x in range(self.x):
                if self.data[y][x]>threshold:
                    self.B[y].append(1)
                else:
                    self.B[y].append(0)
        return self.B
    def ftr(self,B1,col1=True,col2=False,col3=False,n1=3,n2=2):
        '''B1:the two dimension binary array;
           n1:number of zero around the chosen zero;
           col/n2:whether use the col method(
               if total number of zero in one row is less than n2,
               then the row will all be one
           col2:if the upper and lower point of a zero is one,
               then the zero will be one'''
        ay=len(B1)
        ax=len(B1[0])
        '''#降噪法1'''
        def cal1(y,x):
            count=0
            if x!=0 and y!=0:
                point=[(y-1,x-1),(y-1,x),(y-1,x+1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)]
            elif x==0 and y!=0:
                point=[(y-1,x),(y-1,x+1),(y,x+1),(y+1,x),(y+1,x+1)]
            elif x!=0 and y==0:
                point=[(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)]
            else:
                point=[(y,x+1),(y+1,x),(y+1,x+1)]
            for p in point:
                try:
                    if B1[p[0]][p[1]]==0:
                        count+=1
                except:
                    pass
            if count<n1:
                B1[y][x]=1
        '''#降噪法2'''
        def colfilter(y,x):
            count=0
            if B1[y-1][x]==1 and B1[y+1][x]==1:
                B1[y][x]=1
            if count:
                mark=[0,0]
                for y in range(ay):
                    mark[0]+=1-B1[y][x-1]
                    mark[1]+=1-B1[y][x+1]
                if mark[0]>3 or mark[1]>3:
                    B1[y][x]=1      
        '''#降噪法3'''
        def cal2(y,x):
            count=0
            point=[(y,x-1),(y,x+1),(y-1,x),(y+1,x)]
            for p in point:
                try:
                    if B1[p[0]][p[1]]==0:
                        count+=1
                except:
                    pass
            if count<2:
                B1[y][x]=1
            else:
                B1[y][x]=0
        '''#main'''
        if col1:
            for y in range(ay):
                for x in range(ax):
                    if B1[y][x]==0:
                        cal1(y,x)
        if col2:
            for y in range(ay):
                for x in range(ax):
                    if B1[y][x]==0:
                        colfilter(y,x)
        if col3:
            for y in range(ay):
                for x in range(ax):
                    if B1[y][x]==0:
                        cal2(y,x)
        
        return B1
    def reshape(self,B):
        BB=[]
        #直接去除上下两侧冗余
        for y in range(len(B)):
            if B[y].count(0)>5:
                BB.append(B[y])
        #去除两侧冗余并划分数字
        mark=self.cut(BB)
        #排除特殊情况
        double=0
        single=0
        brea=0
        lenmark=[]
        lsum=0
        for i in mark:
            lenmark.append(len(i))
            lsum+=len(i)
        lmax=max(lenmark)
        lmin=min(lenmark)
        if len(mark)==1:
            single=1
        #2,1,1
        if len(mark)==self.number-1:
            double=1
            ff=1
        #2,2或3,1
        elif len(mark)==self.number-2:
            double=1
            ff=2
        #1,1,1,0.5,0.5
        elif len(mark)==5:
            brea=1
        #1,1,1,0.5,0.5
        if brea:
            d1=lenmark.index(min(lenmark))
            if d1==0:
                d2=1
            elif d1==(len(lenmark)-1):
                d2=len(lenmark)-2
            else:
                if lenmark[d1-1]>lenmark[d1+1]:
                    d2=d1+1
                else:
                    d2=d1-1
            if d1<d2:
                mark[d1]=mark[d1]+mark[d2]
            else:
                mark[d1]=mark[d2]+mark[d1]
            mark.pop(d2)
        if double:
            seg=[]
            if ff==1:
                seg.append(lenmark.index(max(lenmark)))
                flag13=0
            elif ff==2:
                if lmax/lmin<1.3:
                    seg=[0,1]
                    flag13=0
                else:
                    seg.append(lenmark.index(max(lenmark)))
                    flag13=1
            if flag13:
                backup=[mark[1-seg[0]]]
                segpoint=int(round((len(mark[seg[0]])/3.0)))
                se=range(0,len(mark[seg[0]]),segpoint)
                if len(se)==3:
                    se.append(len(mark[seg[0]]))
                elif len(se)==4:
                    se[-1]=len(mark[seg[0]])
                iii=1
                for i in range(3):
                    backup.append(mark[seg[0]][se[iii-1]:se[iii]])
                    iii+=1
                mark=backup
            else:
                seg.reverse()
                for se in seg:
                    segpoint=int(len(mark[se])/2.0)
                    mark.insert(se,mark[se][:segpoint+1])
                    mark[se+1]=mark[se+1][segpoint+1:]
        if single:
            backup=[]
            segpoint=int(round((len(mark[0])/4.0)))
            se=range(0,len(mark[0]),segpoint)
            if len(se)==4:
                se.append(len(mark[0]))
            elif len(se)==5:
                se[-1]=len(mark[0])
            iii=1
            for i in range(4):
                backup.append(mark[0][se[iii-1]:se[iii]])
                iii+=1
            mark=backup
        #生成每个数字的二进制二维数组           
        verifycode=[]
        back=[]
        h=len(BB)
        for i in range(len(mark)):
            verifycode.append([])
            back.append([])
            for j in range(h):
                verifycode[i].append([])
        for i in range(len(mark)):
            for k in range(h):
                for j in mark[i]:
                    verifycode[i][k].append(BB[k][j])
        #如果切除过再次过滤
        if double:
            for i in range(len(verifycode)):
                verifycode[i]=self.ftr(verifycode[i])
        #每个数字的修正
        for i in range(len(verifycode)):
            for y in range(len(verifycode[i])):
                count=0
                for x in range(len(verifycode[i][0])):
                    if verifycode[i][y][x]==0:
                        count+=1
                if count>0:
                    back[i].append(verifycode[i][y])
            back[i]=self.sheer(back[i])
        verifycode=back
        return verifycode
    def compensate(self,B):
        def compen(y,x):
            count=0
            point=[(y,x-1),(y,x+1),(y-1,x),(y+1,x)]
            for p in point:
                try:
                    if B[p[0]][p[1]]==0:
                        count+=1
                except:
                    pass
            if count>=3:
                B[y][x]=0
        ay=len(B)
        ax=len(B[0])
        for x in range(ax):
            for y in range(ay):
                if B[y][x]==1:
                    compen(y,x)
        return B
    def cut(self,B):
        index=-1
        xlast=0
        mark=[]
        h=len(B)
        for x in range(len(B[0])):
            count=0
            for y in range(h):
                if B[y][x]==0:
                    count+=1
            if count>0:
                if x-xlast>1 :
                    index+=1
                    mark.append([])
                mark[index].append(x)
                xlast=x
        return mark
    def sheer(self,B):
        ax=len(B[0])
        ay=len(B)
        temp=[]
        for x in range(ax):
            count=0
            for y in range(ay):
                if B[y][x]==0:
                    count+=1
            if count>0:
                temp.append(x)
        for y in range(ay):
            B[y]=B[y][temp[0]:temp[-1]+1]
        return B
    def printfo(self):
        n=0
        for i in range(self.y):
            for j in range(self.x):
                print "%03d"%self.colorlist[n],
                n+=1
            print
def prB(B):
    for y in range(len(B)):
        for x in range(len(B[1])):
            print B[y][x],
        print
    print
def writedown(b,ax=0,ay=0,mode=3):
    f=open("im.py","w")
    if mode==3:
        for i in b:
            for y in range(len(i)):
                for x in range(len(i[0])):
                    f.write(str(i[y][x]))
                f.write('\n')
            f.write('\n')
    elif mode==2:
        for y in range(len(b)):
            for x in range(len(b[0])):
                f.write(str(b[y][x]))
            f.write('\n')
    elif mode==1:
        n=0
        for y in range(ay):
            for x in range(ax):
                t="%03d"%b[n]
                f.write(t)
                n+=1
            f.write('\n')
    f.close()
if __name__=='__main__':
    im=getBI(os.getcwd()+'/useful/004.png',4)
    im.resizee()
    t=im.getB()
    B2=im.ftr(t)
    B3=im.ftr(B2,col1=False,col2=False,col3=True,n1=3,n2=3)
    B2=im.compensate(B2)
    b4=im.reshape(B3)
    for i in range(len(b4)):
      prB(b4[i])

        
    
    


