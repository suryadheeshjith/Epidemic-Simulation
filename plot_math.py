import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

false_neg = 0.1
false_pos = 0.1
lambda_ = 0.01
ntpa_max=6
napt_max=6
ntpa_start=1
X=np.arange(1, napt_max+1, 1)
Y=np.arange(ntpa_start, ntpa_max+1, 1)
X,Y = np.meshgrid(X,Y)
print(X)
print(Y)


def dummy_plot(i,j):
    return i+j

def non_infected_value(false_neg, false_pos, lambda_, napt, ntpa, pos= True):
    val = 0.0
    val = ((1 - false_neg) + (1 - lambda_)**(napt-1)*(false_pos + false_neg-1))**ntpa
    if pos:
        return val
    else:
        return 1-val



def infected_value(false_neg, false_pos, lambda_, napt, ntpa, pos= True):
    val = 0.0
    val = (1 - false_neg)**ntpa
    if pos:
        return val
    else:
        return 1-val



arr = np.zeros((napt_max,ntpa_max))
for i in range(1,napt_max+1):
    for j in range(1,ntpa_max+1):
        # arr[i-1][j-1] = dummy_plot(i,j)
        # arr[i-1][j-1] = non_infected_value(false_neg, false_pos, lambda_, i, j, pos= True)
        # arr[i-1][j-1] = non_infected_value(false_neg, false_pos, lambda_, i, j, pos= False)
        # arr[i-1][j-1] = infected_value(false_neg, false_pos, lambda_, i, j, pos= True)
        arr[i-1][j-1] = infected_value(false_neg, false_pos, lambda_, i, j, pos= False)

print(arr)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, np.array(arr), cmap=cm.coolwarm,linewidth=0, antialiased=False)
plt.xlabel("Number of Agents per testtube")
plt.ylabel("Number of testtubes per agent")
# plt.title("Pool testing strategies vs Probability of positive certificate for non-infected")
# plt.title("Pool testing strategies vs Probability of negative certificate for non-infected")
# plt.title("Pool testing strategies vs Probability of positive certificate for infected")
plt.title("Pool testing strategies vs Probability of negative certificate for infected")
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
