SQRTOOLS_VERSION="0.0.0" #Testbed version
propname=["HP","攻","防","速","敏","魔","抗","智"]
sklname=["火球","冰冻","雷击","地裂","吸血","投毒","连击","会心","瘟疫","命轮","狂暴","魅惑","加速","减速","诅咒","治愈","苏生","净化","铁壁","蓄力","聚气","潜行","血祭","分身","幻术","防御","守护","反弹","护符","护盾","反击","吞噬","亡灵","垂死","隐匿","空技能","空技能","空技能","空技能","空技能"]
class Name:
    def __init__(self):
        self.__val=[]
        self.namebase:int=[0]*128
        self.namebonus:int=[0]*128
        self.nameprop:int=[0]*8
        self.__sklid=[]
        self.__sklfreq=[]
        self.__sklflag=[]
        self.nameskill:list[tuple[int,int]]=[(0,0)]*16
    def load(self,namein:str)->bool:
        if namein=="" or namein.count('@')>1:
            return False
        namein=list(namein.rpartition('@'))
        if namein[1]=='@':
            if namein[2]=='':
                namein[2]=namein[0]
        else:
            namein[0]=namein[2]
        namestr=list(namein[0].encode())
        teamstr=list(namein[2].encode())
        namestr.insert(0,0)
        teamstr.insert(0,0)
        namelen=len(namestr)
        teamlen=len(teamstr)
        if namelen>256 or teamlen>256:
            return False
        self.__val=list(range(256))
        s=0
        for i in range(256):
            s+=(teamstr[i%teamlen]+self.__val[i])
            s%=256
            self.__val[i],self.__val[s]=self.__val[s],self.__val[i]
        for i in range(2):
            s=0
            for j in range(256):
                s+=(namestr[j%namelen]+self.__val[j])
                s%=256
                self.__val[j],self.__val[s]=self.__val[s],self.__val[j]
        s=0
        for i in range(256):
            m=(self.__val[i]*181+160)%256
            if m>=89 and m<217:
                self.namebase[s]=m&63
                s+=1
        self.namebonus[:]=self.namebase[:]
        return True
    def calcprops(self,usebonus:bool)->None:
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
    def calcskill(self,usebonus:bool)->None:
        self.__sklid=list(range(0,40))
        self.__sklfreq=[0]*16
        self.__sklflag=[True]*16
        a=b=0
        randbase=[]
        randbase[:]=self.__val[:]
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
            q=min(self.namebase[i],self.namebase[i+1],self.namebase[i+2],self.namebase[i+3])
            if usebonus==True:
                p=min(self.namebonus[i],self.namebonus[i+1],self.namebonus[i+2],self.namebonus[i+3])
            else:
                p=q
            if p>10:
                if self.__sklid[j]<35:
                    self.__sklfreq[j]=p-10
                if q<=10:
                    self.__sklflag[j]=False
                elif self.__sklid[j]<25:
                    last=j
            j+=1
        if last!=-1:
            self.__sklflag[last]=False
            self.__sklfreq[last]*=2
        if usebonus==True:
            info=self.namebonus
        else:
            info=self.namebase
        if self.__sklfreq[14]>0 and self.__sklflag[14]:
            self.__sklfreq[14]+=min(info[60],info[61],self.__sklfreq[14])
            self.__sklflag[14]=False
        if self.__sklfreq[15]>0 and self.__sklflag[15]:
            self.__sklfreq[15]+=min(info[62],info[63],self.__sklfreq[15])
            self.__sklflag[15]=False
        self.nameskill=list(zip(self.__sklid[0:16],self.__sklfreq))
        return
if __name__=="__main__":
    import cmd
    from operator import itemgetter
    from sys import exit
    class Reader(cmd.Cmd):
        intro="sqrtools - 名字竞技场小工具\nTestbed | sqrt2802, 2025.\n\n输入 help 以获取用法说明\n"
        prompt='>'
        def emptyline(self):
            return
        def do_exit(self,arg):
            exit()
            return
        def do_help(self,arg):
            print("\n命令列表:\nconv - 转换器快捷方式\nbase - 数值来源与加成潜力查询\naddon - 组队加成计算\npeek - 查看 val/namebase\nhelp - 获取帮助\nexit - 退出\n")
            print("除 addon, help 和 exit 外的计算命令格式均为 <命令名称> <名字>\naddon 命令格式为 addon <加号分隔的战组>, 也可以不附加参数进入交互输入模式\n")
            return
        def do_peek(self,arg):
            if arg=='':
                strin=input("输入名字: ")
            else:
                strin=arg
            name=Name()
            if not name.load(strin):
                print("名字载入出错\n")
                return
            print("\n名字的 val 数值:")
            for i in name._Name__val:
                print(i,end=' ')
            print("\n\n名字的 namebase 数值:")
            for i in name.namebase:
                print(i,end=' ')
            print('\n')
            return
        def do_conv(self,arg):
            if arg=='':
                strin=input("输入名字: ")
            else:
                strin=arg
            name=Name()
            if not name.load(strin):
                print("名字载入出错\n")
                return
            name.calcprops(False)
            for i in range(8):
                print(propname[i],name.nameprop[i],sep='',end=' ')
            cf=(name.nameprop[1]+name.nameprop[3]+name.nameprop[5])*2+name.nameprop[4]+name.nameprop[7]-name.nameprop[2]*2-name.nameprop[6]*2
            print("\n八围",round(name.nameprop[0]/3,1)+sum(name.nameprop[1:8])," 嘲讽值",cf,sep='')
            name.calcskill(False)
            rec=sorted(name.nameskill,key=itemgetter(1),reverse=True)
            for now in rec:
                if now[1]<=0:
                    break
                if now[0]<35:
                    print(sklname[now[0]],now[1],sep='',end=' ')
            print('\n')
            return
        def do_base(self,arg):
            if arg=='':
                strin=input("输入名字: ")
            else:
                strin=arg
            name=Name()
            if not name.load(strin):
                print("名字载入出错\n")
                return
            print()
            r=name.namebase[0:32]
            print("HP:",' '.join(str(i) for i in r[0:10]),sep=' ',end=' ')
            r[0:10]=sorted(r[0:10])
            print("->",154+sum(r[3:7]),'/',154+sum(r[4:8]),sep=' ')
            name.nameprop[0]=154+sum(r[3:7])
            propcnt=1
            for i in range(10,31,3):
                print(propname[propcnt],':',sep='',end=' ')
                print(' '.join(str(j).zfill(2) for j in r[i:i+3]),end=' ')
                r[i:i+3]=sorted(r[i:i+3])
                print("->",r[i+1]+36,'/',r[i+2]+36)
                name.nameprop[propcnt]=r[i+1]+36
                propcnt+=1
            print()
            name.calcskill(False)
            doubleflag=-1
            for i in range(15,-1,-1):
                if name.nameskill[i][1]>0 and name.nameskill[i][0]<25:
                    doubleflag=i
                    break
            for i in range(14):
                print("#",str(i).zfill(2),' ',sklname[name.nameskill[i][0]],sep='',end='')
                if name.nameskill[i][0]>=35:
                    print()
                else:
                    r=name.namebase[i*4+64:i*4+68]
                    print(':',' '.join(str(j).zfill(2) for j in r),"->",end=' ')
                    r=sorted(r)
                    if doubleflag==i:
                        print(str(name.nameskill[i][1]).zfill(2),'/',str((r[1]-10)*2 if r[1]>10 else 0).zfill(2),"(末尾主动)")
                    else:
                        print(str(name.nameskill[i][1]).zfill(2),'/',str(r[1]-10 if r[1]>10 else 0).zfill(2))
            for i in range(14,16):
                print("#",str(i).zfill(2),' ',sklname[name.nameskill[i][0]],sep='',end='')
                if name.nameskill[i][0]>=35:
                    print()
                else:
                    r=name.namebase[i*4+64:i*4+68]
                    print(':',' '.join(str(j).zfill(2) for j in r),"->",end=' ')
                    r=sorted(r)
                    if name.nameskill[i][1]>=0:
                        if doubleflag==i:
                            print(str(name.nameskill[i][1]).zfill(2),'/',str((r[1]-10)*2 if r[1]>10 else 0).zfill(2),"(末尾主动)")
                        else:
                            a=r[1]-10+min([r[1]-10]+name.namebase[32+i*2:34+i*2])
                            b=r[0]-10+min(r[0]-10,max(name.namebase[32+i*2:34+i*2]))
                            print(str(name.nameskill[i][1]).zfill(2),'/',str(a if a>b else b).zfill(2),"(末尾座位加成",' '.join(str(j).zfill(2) for j in name.namebase[32+i*2:34+i*2])+')')
                    else:
                        print(str(name.nameskill[i][1]).zfill(2),'/',str(r[1]-10 if r[1]>10 else 0).zfill(2))
            print()
            return
        def do_addon(self,arg):
            def calcbonus(target,addon):
                for i in range(7,128):
                    if addon[i-1]==target.namebase[i]:
                        target.namebonus[i]=max(target.namebonus[i],addon[i])
                return
            strin=[]
            namelist=[]
            if arg=='':
                print("输入名字, 一行一个号, 空行结束:")
                while True:
                    now=input()
                    if now=='':
                        break
                    strin.append(now)
            else:
                strin=arg.split('+')
            for now in strin:
                namelist.append(Name())
                if not namelist[-1].load(now):
                    print("名字载入出错\n")
                    return
            for i in range(len(namelist)):
                for j in range(i+1,len(namelist)):
                    calcbonus(namelist[i],namelist[j].namebase)
                    calcbonus(namelist[j],namelist[i].namebase)
            print("\n组队数值:\n")
            prop=[]
            bonus=[]
            for i in range(len(namelist)):
                print(strin[i])
                namelist[i].calcprops(False)
                prop[:]=namelist[i].nameprop[:]
                namelist[i].calcprops(True)
                bonus[:]=namelist[i].nameprop[:]
                for j in range(8):
                    print(propname[j],bonus[j],(("(+"+str(bonus[j]-prop[j])+')') if bonus[j]!=prop[j] else ''),sep='',end=' ')
                bw1=round(prop[0]/3,1)+sum(prop[1:8])
                bw2=round(bonus[0]/3,1)+sum(bonus[1:8])
                cf1=(prop[1]+prop[3]+prop[5]-prop[2]-prop[6])*2+prop[4]+prop[7]
                cf2=(bonus[1]+bonus[3]+bonus[5]-bonus[2]-bonus[6])*2+bonus[4]+bonus[7]
                print()
                namelist[i].calcskill(False)
                prop[:]=namelist[i].nameskill[:]
                namelist[i].calcskill(True)
                bonus[:]=namelist[i].nameskill[:]
                sklrec=[]
                for j in range(16):
                    if bonus[j][0]<35 and bonus[j][1]>0:
                        sklrec.append((bonus[j][0],bonus[j][1],bonus[j][1]-prop[j][1]))
                sklrec=sorted(sklrec,key=itemgetter(1),reverse=True)
                for now in sklrec:
                    print(sklname[now[0]],now[1],(("(+"+str(now[2])+')') if now[2]>0 else ''),sep='',end=' ')
                print("\n八围",bw2,(("(+"+str(bw2-bw1)+')') if bw2!=bw1 else ''),sep='',end=' ')
                print("嘲讽值",cf2,(f"({(cf2-cf1):+d})" if cf2!=cf1 else ''),sep='',end='\n\n')
            print()
            return
    Reader().cmdloop()
