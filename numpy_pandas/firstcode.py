from sklearn.linear_model import LinearRegression
import numpy as np
 
x=np.array([[1],[2],[3],[4]])

y=np.array([30,50,70,90])

model=LinearRegression()

model.fit(x,y)

print(model. predict([[5]]))
 