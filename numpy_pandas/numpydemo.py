import numpy as np
list1=np.array([10,20,30,40])
list2=np.array([10,20,70,90])

print(list2[-2])
list3=list1+list2
print(list3)
print(20 in list1)
print(np.where(list1==20))
print(list1[1:3])