SQRTOOLS_VERSION="0.0.0" #Testbed version
class Name:
    def __init__(self):
        self.val=list(range(256))
        self.namebase=[0]*128
        self.__namestr=[0]*256
        self.__teamstr=[0]*256
        self.__namelen=0
        self.__teamlen=0
        self.nameprop=[0]*8
        self.__sklid=list(range(0,40))
        self.__sklfreq=[0]*40
        self.nameskill=[(-1,0)]*40
        self.reusable=False
        self.__reusablestate=False
        self.__lock=0
    def check(self,namein:str)->int:
        if self.__lock==0:
            self.__reusablestate=self.reusable
        if not self.__reusablestate:
            if self.__lock!=0:
                return 1
        self.__lock=1
        if namein=="":
            return -1
        if namein.count('@')>1:
            return -2
        namein=list(namein.rpartition('@'))
        if len(namein[0])>255 or len(namein[2])>255:
            return -3
        if namein[1]=='@':
            if namein[2]=='':
                namein[2]=namein[0]
        else:
            namein[0]=namein[2]
        namein[0]=namein[0].encode()
        namein[2]=namein[2].encode()
        self.__namelen=len(namein[0])
        self.__teamlen=len(namein[2])
        for i in range(self.__namelen):
            self.__namestr[i+1]=namein[0][i]
        for i in range(self.__teamlen):
            self.__teamstr[i+1]=namein[2][i]
        self.__namelen+=1
        self.__teamlen+=1
        return 0
    def load(self)->bool:
        if self.__reusablestate:
            if self.__lock<1:
                return False
            self.val=list(range(256))
        elif self.__lock!=1:
            return False
        self.__lock=2
        s=0
        for i in range(256):
            s+=(self.__teamstr[i%self.__teamlen]+self.val[i])
            s%=256
            self.val[i],self.val[s]=self.val[s],self.val[i]
        for i in range(2):
            s=0
            for j in range(256):
                s+=(self.__namestr[j%self.__namelen]+self.val[j])
                s%=256
                self.val[j],self.val[s]=self.val[s],self.val[j]
        s=0
        for i in range(256):
            m=(self.val[i]*181+160)%256
            if m>=89 and m<217:
                self.namebase[s]=m&63
                s+=1
        return True
    def calcprops(self)->bool:
        if self.__lock<2:
            return False
        propcnt=1
        r=self.namebase[0:32]
        for i in range(10,31,3):
            r[i:i+3]=sorted(r[i:i+3])
            self.nameprop[propcnt]=r[i+1]
            propcnt+=1
        r[0:10]=sorted(r[0:10])
        self.nameprop[0]=154
        for i in range(3,7):
            self.nameprop[0]+=r[i]
        for i in range(1,8):
            self.nameprop[i]+=36
        return True
    def calcskill(self)->bool:
        if self.__reusablestate:
            if self.__lock<2:
                return False
            self.__sklid=list(range(0,40))
            self.__sklfreq=[0]*40
        elif self.__lock!=2:
            return False
        self.__lock=3
        a=b=0
        randbase=[]
        randbase[:]=self.val[:]
        def randgen():
            nonlocal a,b,randbase
            def m():
                nonlocal a,b,randbase
                a=(a+1)%256
                b=(b+randbase[a])%256
                randbase[a],randbase[b]=randbase[b],randbase[a]
                return randbase[(randbase[a]+randbase[b])&255]
            return ((m()<<8)|m())%40
        s=0
        for i in range(2):
            for j in range(40):
                s=(s+randgen()+self.__sklid[j])%40
                self.__sklid[j],self.__sklid[s]=self.__sklid[s],self.__sklid[j]
        last=-1
        j=0
        for i in range(64,128,4):
            p=min(self.namebase[i],self.namebase[i+1],self.namebase[i+2],self.namebase[i+3])%256
            if p>10 and self.__sklid[j]<35:
                self.__sklfreq[j]=p-10
                if self.__sklid[j]<25:
                    last=j
            j+=1
        if last!=-1:
            self.__sklfreq[last]*=2
        if self.__sklfreq[14]>0 and last!=14:
            self.__sklfreq[14]+=min(self.namebase[60],self.namebase[61],self.__sklfreq[14])
        if self.__sklfreq[15]>0 and last!=15:
            self.__sklfreq[15]+=min(self.namebase[62],self.namebase[63],self.__sklfreq[15])
        self.nameskill=list(zip(self.__sklid,self.__sklfreq))
        return True
class NameDev:
    def __init__(self):
        self.val=[]
        self.namebase=[0]*128
        self.namebonus=[0]*128
        self.namestr=[0]*256
        self.teamstr=[0]*256
        self.namelen=0
        self.teamlen=0
        self.nameprop=[0]*8
        self.sklid=[]
        self.sklfreq=[]
        self.sklflag=[]
        self.nameskill=[]
    def check(self,namein):
        if namein=="":
            return -1
        if namein.count('@')>1:
            return -2
        namein=list(namein.rpartition('@'))
        if len(namein[0])>255 or len(namein[2])>255:
            return -3
        if namein[1]=='@':
            if namein[2]=='':
                namein[2]=namein[0]
        else:
            namein[0]=namein[2]
        namein[0]=namein[0].encode()
        namein[2]=namein[2].encode()
        self.namelen=len(namein[0])
        self.teamlen=len(namein[2])
        for i in range(self.namelen):
            self.namestr[i+1]=namein[0][i]
        for i in range(self.teamlen):
            self.teamstr[i+1]=namein[2][i]
        self.namelen+=1
        self.teamlen+=1
        return 0
    def load(self):
        self.val=list(range(256))
        s=0
        for i in range(256):
            s+=(self.teamstr[i%self.teamlen]+self.val[i])
            s%=256
            self.val[i],self.val[s]=self.val[s],self.val[i]
        for i in range(2):
            s=0
            for j in range(256):
                s+=(self.namestr[j%self.namelen]+self.val[j])
                s%=256
                self.val[j],self.val[s]=self.val[s],self.val[j]
        s=0
        for i in range(256):
            m=(self.val[i]*181+160)%256
            if m>=89 and m<217:
                self.namebase[s]=m&63
                s+=1
        self.namebonus[:]=self.namebase[:]
        return
    def calcprops(self,usebonus):
        propcnt=1
        if usebonus==True:
            r=self.namebonus[0:32]
        else:
            r=self.namebase[0:32]
        for i in range(10,31,3):
            r[i:i+3]=sorted(r[i:i+3])
            self.nameprop[propcnt]=r[i+1]
            propcnt+=1
        r[0:10]=sorted(r[0:10])
        self.nameprop[0]=154
        for i in range(3,7):
            self.nameprop[0]+=r[i]
        for i in range(1,8):
            self.nameprop[i]+=36
        return
    def calcskill(self,usebonus):
        self.sklid=list(range(0,40))
        self.sklfreq=[0]*40
        self.sklflag=[True]*40
        a=b=0
        randbase=[]
        randbase[:]=self.val[:]
        def randgen():
            nonlocal a,b,randbase
            def m():
                nonlocal a,b,randbase
                a=(a+1)%256
                b=(b+randbase[a])%256
                randbase[a],randbase[b]=randbase[b],randbase[a]
                return randbase[(randbase[a]+randbase[b])&255]
            return ((m()<<8)|m())%40
        s=0
        for i in range(2):
            for j in range(40):
                s=(s+randgen()+self.sklid[j])%40
                self.sklid[j],self.sklid[s]=self.sklid[s],self.sklid[j]
        last=-1
        j=0
        for i in range(64,128,4):
            q=min(self.namebase[i],self.namebase[i+1],self.namebase[i+2],self.namebase[i+3])%256
            if usebonus==True:
                p=min(self.namebonus[i],self.namebonus[i+1],self.namebonus[i+2],self.namebonus[i+3])%256
            else:
                p=q
            if p>10:
                if self.sklid[j]<35:
                    self.sklfreq[j]=p-10
                if q<=10:
                    self.sklflag[j]=False
                elif self.sklid[j]<25:
                    last=j
            j+=1
        if last!=-1:
            self.sklflag[last]=False
            self.sklfreq[last]*=2
        if self.sklfreq[14]>0 and self.sklflag[14]:
            self.sklfreq[14]+=min(self.namebonus[60],self.namebonus[61],self.sklfreq[14])
            self.sklflag[14]=False
        if self.sklfreq[15]>0 and self.sklflag[15]:
            self.sklfreq[15]+=min(self.namebonus[62],self.namebonus[63],self.sklfreq[15])
            self.sklflag[15]=False
        self.nameskill=list(zip(self.sklid,self.sklfreq))
        return
if __name__=="__main__":
    import cmd
    from operator import itemgetter
    from sys import exit
    def errcatch(errcode):
        if errcode==0:
            return True
        elif errcode<0 and errcode>=-3:
            errmsg={-1:"错误: 输入不能为空。",-2:"错误: 无法分割名字与战队名，请检查输入。",-3:"错误: 名字或战队名长度过大。"}
            print(errmsg[errcode])
        else:
            print("错误：未知错误。")
        return False
    def lockcatch(status):
        if not status:
            print("错误：未知错误。")
            return False
        else:
            return True
    def prop(namearg,verbose):
        name=Name()
        if errcatch(name.check(namearg))==False:
            return
        propname=["HP","攻","防","速","敏","魔","抗","智"]
        if lockcatch(name.load())==False:
            return
        if lockcatch(name.calcprops())==False:
            return
        for i in range(8):
            if verbose:
                print(propname[i],end='')
            print(name.nameprop[i],end=' ')
        print()
        if verbose:
            print("八围",round(name.nameprop[0]/3,1)+sum(name.nameprop[1:8])," 嘲讽值",name.nameprop[1]+name.nameprop[3]+name.nameprop[5]+(name.nameprop[4]+name.nameprop[7])/2-name.nameprop[2]-name.nameprop[6],sep='')
        return
    def skill(namearg):
        name=Name()
        if errcatch(name.check(namearg))==False:
            return
        sklname=["火球","冰冻","雷击","地裂","吸血","投毒","连击","会心","瘟疫","命轮","狂暴","魅惑","加速","减速","诅咒","治愈","苏生","净化","铁壁","蓄力","聚气","潜行","血祭","分身","幻术","防御","守护","反弹","护符","护盾","反击","吞噬","亡灵","垂死","隐匿","空","空","空","空","空"]
        if lockcatch(name.load())==False:
            return
        if lockcatch(name.calcskill())==False:
            return
        rec=sorted(name.nameskill,key=itemgetter(1),reverse=True)
        for now in rec:
            if now[1]<=0:
                break
            if now[0]<35:
                print(sklname[now[0]],now[1],sep='',end=' ')
        print()
        return
    def peek(namearg):
        name=Name()
        if errcatch(name.check(namearg))==False:
            return
        if lockcatch(name.load())==False:
            return
        print("名字的 val 数值:",end=' ')
        for i in name.val:
            print(i,end=' ')
        print("\n名字的 namebase 数值:",end=' ')
        for i in name.namebase:
            print(i,end=' ')
        print()
        return
    class Reader(cmd.Cmd):
        intro="sqrtools - 名字竞技场小工具\nTestbed | sqrt2802, 2024.\n"
        prompt='>'
        def emptyline(self):
            return
        def do_exit(self,arg):
            exit()
            return
        def do_help(self,arg):
            print("命令列表:\nprop - 计算名字属性\nskill - 计算名字技能\npeek - 查看计算中间产物\nconv - 转换器快捷方式\nhelp - 获取帮助\nexit - 退出")
            return
        def do_prop(self,arg):
            arg=arg.split()
            if(len(arg)!=1):
                print("用法: prop <名字> 或 prop -i\n直接输入的名字不能含有空格。如果有，使用选项 -i 进入交互式输入。")
                return
            if arg[0]=="-i":
                arg[0]=input("输入名字: ")
            prop(arg[0],False)
            return
        def do_skill(self,arg):
            arg=arg.split()
            if(len(arg)!=1):
                print("用法: skill <名字> 或 skill -i\n直接输入的名字不能含有空格。如果有，使用选项 -i 进入交互式输入。\n熟练度 >0 的非空技能将会以熟练度降序输出。\n请注意，技能熟练度最高值为 104，与评分输出中的技能发动频率不同。")
                return
            if arg[0]=="-i":
                arg[0]=input("输入名字: ")
            skill(arg[0])
            return
        def do_peek(self,arg):
            arg=arg.split()
            if(len(arg)!=1):
                print("用法: peek <名字> 或 peek -i\n直接输入的名字不能含有空格。如果有，使用选项 -i 进入交互式输入。")
                return
            if arg[0]=="-i":
                arg[0]=input("输入名字: ")
            peek(arg[0])
            return
        def do_conv(self,arg):
            arg=arg.split()
            if(len(arg)!=1):
                print("用法: conv <名字> 或 conv -i\n直接输入的名字不能含有空格。如果有，使用选项 -i 进入交互式输入。")
                return
            if arg[0]=="-i":
                arg[0]=input("输入名字: ")
            prop(arg[0],True)
            skill(arg[0])
            return
    Reader().cmdloop()
