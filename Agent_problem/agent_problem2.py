n=4
# In this problem there are n PA statements, one of which is true
import numpy as np
class Sit:
    def __init__(self,acts):
        acts=np.array(acts)
        self.acts=acts
        assert acts.size==(1<<n),(acts.size,(1<<n))
        #self.des=np.full([1<<n],(1<<n)-1,np.uint64)

        self.des=1<<acts
        #print(self.des)
        r=np.arange(1<<n)
        for i in range(n):
            s=(r>>i)&1
            self.des[s==1]|=self.des[s==0]
            #print(i,self.des)
    def get(self):
        a=0#(1<<n)-1
        #000=contradiction
        #111=max uncertainty
        for i in range((1<<n)+1):
            #print(i,a)
            b=self.des[a]
            if b==a:
                return (int(a),self.acts[a])
            a=b
        else:
            print("error")
    def explain(self):
        i,r=self.get()
        strs=["CC ","CD ","DC ","DD "]
        strs2=[(" "*len(s),s) for s in strs]
        print("".join(strs2[j][(i>>j)&1] for j in range(4))+" :"+strs[r])
def build():
    l=[chr(ord("a")+i) for i in range(n)]
    ls=np.zeros([1<<n],np.uint64)
    for i in range(1<<n):
        pu=input("[]"+",".join(s for j,s in enumerate(l) if (i>>j)&1==1)+" |- ")
        ls[i]=l.index(pu)
    return Sit(ls)
#b=build()
#01 10 01 10
# 1  0  1  0
#00 01 10 11
#b=Agent(np.array([1, 0, 1, 0], dtype=np.uint64))
#b.get()
class Agent:
    #00=both coop
    #01=i defect
    #10= i coop
    #11=both defect
    #An agent is defined by 16 bits, indicating what it does in each circumstance.
    #so the 0000 th bit indicates what you do in a contradiction.
    #the 0001 bit, what you do if you prove you both coop
    #the 1111 bit, what you do if you can't prove anything
    def __init__(self,acts):
        self.acts=acts
        assert acts.size==16
    def coify(self):
        a=self.acts
        #swaps bits 1 and 2 in index.
        b=a[[0,1,4,5,2,3,6,7,8,9,12,13,10,11,14,15]]
        return coAgent(b)
    def combine_(self,other):
        sacts=self.acts
        if not isinstance(other, coAgent):
            other=other.coify()

        oacts=other.acts

        return Sit(sacts+2*oacts)#.get()
    def combine(self,other):
        return self.combine_(other).get()
    def play(self,other):
        self.combine_(other).explain()
    def explain(self):
        print("possibilities I can't disprove  : response")
        print("Other Self, ie CD is when I win big.")
        strs=["CC ","CD ","DC ","DD "]
        strs=[(" "*len(s),s) for s in strs]
        for i in range(16):
            print("".join(strs[j][(i>>j)&1] for j in range(4))+" :"+"CD"[self.acts[i]])
class coAgent:
    #00=both coop
    #01=i coop
    #10= i defect
    #11=both defect
    #An agent is defined by 16 bits, indicating what it does in each circumstance.
    #so the 0000 th bit indicates what you do in a contradiction.
    #the 0001 bit, what you do if you prove you both coop
    #the 1111 bit, what you do if you can't prove anything
    def __init__(self,acts):
        self.acts=acts
        assert acts.size==16
        
defectBot=Agent(np.ones([16],np.uint64))#.coify()
cooperateBot=Agent(np.zeros([16],np.uint64))#.coify()
f=Agent(np.array([0,0,0,0]+[1]*12,np.uint64))#.coify()#fairbot
d=defectBot
c=cooperateBot
def test(b):
    r=b.combine(c)
    assert r in (0,1)
    print("c",r,1)
    r=b.combine(d)
    assert r in (2,3)
    print("d",r,2)
    r=b.combine(f)
    assert r in (0,3)
    print("f",r,0)
    r=b.combine(b)
    assert r in (0,3)
    print("b",r,0)
    print(b.acts)
good_a=[]
for i in range(0):#1<<16):
    b=Agent(np.array([(i>>j)&1==1 for j in range(16)],np.uint64))
    _,r=b.combine(c)
    assert r in (0,1)
    if r==0:
        continue
    #defects against cooperate_bot
    _,r=b.combine(d)
    assert r in (2,3)
    if r==2:
        continue
    _,r=b.combine(f)
    assert r in (0,2,3)
    if r==3:
        continue
    _,r=b.combine(b)
    assert r in (0,3)
    if r==3:
        continue
    #print(b.acts)
    good_a.append(b)

import pickle 
with open("good_agents.pickle","rb") as file:
    good_a=pickle.load(file)
loosers=set()
for i in range(0):#len(good_a)):
    if i%10==0:
        print(i,len(good_a))
    for j in range(i+1):
        _,r=good_a[i].combine(good_a[j])
        if r==1:
            loosers.add(j)
        elif r==2:
            loosers.add(i)
with open("best_agents.pickle","rb") as file:
    best=pickle.load(file)
best_c=[0]*len(best)
for i in range(0):#len(best)):
    for j in range(i+1):
        _,r=best[i].combine(best[j])
        assert r in (0,3)
        if r==0:
            best_c[i]+=1
            best_c[j]+=1
print(best_c)
with open("bester_agents.pickle","rb") as file:
    bester=pickle.load(file)
scores=[[0]*4 for i in range(len(bester))]
for i in range(len(bester)):
    gb=bester[i]
    print(i)
    for j in range(1<<16):
        b=Agent(np.array([(j>>k)&1==1 for k in range(16)],np.uint64))
        _,r=gb.combine(b)
        scores[i][r]+=1
