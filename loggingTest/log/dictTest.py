#--*--coding:utf-8--*--
from multiprocessing import Process

busimap={}
def busimaptest():
    doc = int(input("input numbers:"))
    circle=int(input("int put circle times:"))
    for m in range(circle):
        if m==circle-1:
            print(busimap)
        for i in range(doc):
            docname='doc%s'%i
            busimap[docname]=i
        print(busimap)

def mutibusimap():
    # doc = int(input("input numbers:"))
    # for i in range(doc):
    p = Process(target=busimaptest)
        # p = Process(target=busimaptest, args=(i.__str__(),))
    p.start()


if __name__ == '__main__':
   li=[1, 2, 3, 4, 5]

   print(sum(li)/len(li))