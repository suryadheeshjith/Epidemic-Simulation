import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

ntpa_max=6
napt_max=6
ntpa_start=1
X=np.arange(1, napt_max+1, 1)
Y=np.arange(ntpa_start, ntpa_max+1, 1)
X,Y = np.meshgrid(X,Y)
print(X)
print(Y)

data_list={'Infected': np.array([[112.1       ,  65.13333333,  46.6       ,  40.46666667,
         37.13333333,  34.76666667],
       [169.86666667, 116.36666667,  79.8       ,  66.36666667,
         54.1       ,  48.6       ],
       [208.36666667, 146.9       , 120.76666667,  92.8       ,
         71.5       ,  67.46666667],
       [230.56666667, 182.56666667, 140.9       , 124.4       ,
         98.13333333,  84.46666667],
       [239.36666667, 180.66666667, 168.56666667, 147.36666667,
        117.86666667,  99.        ],
       [251.83333333, 204.1       , 177.66666667, 162.56666667,
        131.93333333, 114.8       ]]), 'False Positives': np.array([[0.00000000e+00, 8.96000000e+01, 1.88566667e+02, 3.44433333e+02,
        5.29366667e+02, 7.34400000e+02],
       [0.00000000e+00, 2.56666667e+00, 8.86666667e+00, 2.08666667e+01,
        3.28666667e+01, 5.03000000e+01],
       [0.00000000e+00, 3.33333333e-02, 1.23333333e+00, 2.66666667e+00,
        4.56666667e+00, 8.43333333e+00],
       [0.00000000e+00, 0.00000000e+00, 1.66666667e-01, 8.66666667e-01,
        1.10000000e+00, 1.73333333e+00],
       [0.00000000e+00, 0.00000000e+00, 6.66666667e-02, 4.00000000e-01,
        5.00000000e-01, 9.33333333e-01],
       [0.00000000e+00, 0.00000000e+00, 3.33333333e-02, 2.00000000e-01,
        4.33333333e-01, 4.66666667e-01]]), 'Quarantined': np.array([[ 444.63333333,  830.03333333, 1006.86666667, 1260.16666667,
        1455.86666667, 1634.3       ],
       [ 372.96666667,  478.        ,  486.93333333,  533.8       ,
         523.43333333,  540.86666667],
       [ 297.1       ,  389.63333333,  483.7       ,  483.13333333,
         462.1       ,  492.06666667],
       [ 243.5       ,  386.9       ,  426.1       ,  506.66666667,
         479.66666667,  455.06666667],
       [ 207.4       ,  297.06666667,  417.8       ,  485.76666667,
         474.93333333,  448.96666667],
       [ 186.96666667,  297.9       ,  398.53333333,  436.5       ,
         453.66666667,  460.16666667]])}


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, np.array(data_list['False Positives']), cmap=cm.coolwarm,linewidth=0, antialiased=False)
plt.xlabel("Number of Agents per testtube")
plt.ylabel("Number of testtubes per agent")
plt.title("Pool testing strategies vs total false positives")
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, np.array(data_list['Infected']), cmap=cm.coolwarm,linewidth=0, antialiased=False)
plt.xlabel("Number of Agents per testtube")
plt.ylabel("Number of testtubes per agent")
plt.title("Pool testing strategies vs total infections")
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, np.array(data_list['Quarantined']), cmap=cm.coolwarm,linewidth=0, antialiased=False)
plt.xlabel("Number of Agents per testtube")
plt.ylabel("Number of testtubes per agent")
plt.title("Pool testing strategies vs total quarantine")
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
