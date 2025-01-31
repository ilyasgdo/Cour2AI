import matplotlib.pyplot as plt

x = [n for n in range(1, 101)]  
y = [(-1) / n for n in range(1, 101)]  

plt.scatter(x, y)

plt.show()