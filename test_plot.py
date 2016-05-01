import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline


def fnx():
    return np.random.randint(5, 50, 10)

x = np.arange(10)

y = np.row_stack((fnx(), fnx(), fnx()))
y1, y2, y3 = fnx(), fnx(), fnx()

xnew = np.linspace(x.min(),x.max(),300)

y11= spline(x,y1,xnew)
y21= spline(x,y2,xnew)
y31= spline(x,y3,xnew)

y_new = np.zeros((3,300))
for i in range(3):
    y_new[i,:]=spline(x,y[i,:],xnew)

print y_new
fig, ax = plt.subplots()
ax.stackplot(xnew, y_new)
plt.show()