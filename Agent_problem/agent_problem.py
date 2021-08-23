n=2# In this problem there are n PA statements, one of which is false.
import numpy as np
class Agent:
    def __init__(self,acts):
        acts=np.array(acts)
        self.acts=acts
        assert acts.size==(1<<n)
        self.des=np.full([1<<n],(1<<n)-1,np.uint64)
        print(self.des)
        self.des-=1<<acts
        print(self.des)
        r=np.arange(1<<n)
        for i in range(n):
            s=(r>>i)&1
            self.des[s==0]&=self.des[s==1]
            print(i,self.des)
    def get(self):
        a=(1<<n)-1
        for i in range((1<<n)+1):
            print(i,a)
            b=self.des[a]
            if b==a:
                return a
            a=b
        else:
            print("error")
def build():
    l=[chr(ord("a")+i) for i in range(n)]
    ls=np.zeros([1<<n],np.uint64)
    for i in range(1<<n):
        pu=input("[]"+",".join(s for j,s in enumerate(l) if (i>>j)&1==1)+" |- ¬")
        ls[i]=l.index(pu)
    return Agent(ls)
b=build()
#01 10 01 10
# 1  0  1  0
#00 01 10 11
#b=Agent(np.array([1, 0, 1, 0], dtype=np.uint64))
b.get()
