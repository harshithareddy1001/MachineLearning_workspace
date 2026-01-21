import numpy as np
list1=np.array([[10,20,30,40],[1,2,3,4],[90,100,110,120]])
list2=np.array([[10,20,70,90],[20,30,40,50],[100,200,300,400]])
list2.resize(4,3)
list1.reshape(4,3)
print(list2[1,:])
list2=list2.reshape(1,12)
print(list2)
print(list1)