import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import matplotlib

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
'''
hdict=[[692.7,514.36,343.52,696.42],
       [5399.28,5194.1,4309.78,5103.02],
       [1071.84,1592.0,1920.72,872.44]]

labels=[(3,2),(4,2),(5,2),'Dynamic']
x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x-width, hdict[0], width, label='Infections')
rects2 = ax.bar(x, hdict[1], width, label='Quarantined Days')
rects4 = ax.bar(x+width, hdict[2], width, label='False Positives')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Pooling Strategy')
ax.set_xlabel('Cumulative Total')
ax.set_title('Comparision of different pooling strategies')

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
plt.show()
plt.savefig('comparision.pgf')

'''
import matplotlib.pyplot as plt
from matplotlib import colors

import matplotlib

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

def legend():
  color_list={(1,1):'cyan',(2,1):'blue',(3,2):'green',(4,2):'pink',(5,2):'orange',(5,3):'red',(6,2):'purple',(6,3):'grey'}
  fig,ax=plt.subplots()
  points=[]
  for c in color_list.keys():
    points.append(ax.scatter(0,0,color=color_list[c],s=20,alpha=0.8,edgecolors='none'))
  legendFig = plt.figure("Legend plot")
  legendFig.legend(points, color_list.keys(), loc='center')
  legendFig.savefig('legend.pgf')

#legend()

def plot(X,Y,Z,title='',xlabl='',ylabl=''):
  color_list={(1,1):'cyan',(2,1):'blue',(3,2):'green',(4,2):'pink',(5,2):'orange',(5,3):'red',(6,2):'purple',(6,3):'grey'}
  fig,ax=plt.subplots()
  for i in range(len(X)):
    ax.scatter(X[i],Y[i],color=color_list[Z[i]],s=20,alpha=0.8,edgecolors='none')
  #ax.legend(color_list.keys())
  #ax.grid(True)
  plt.xlabel(xlabl)
  plt.ylabel(ylabl)
  plt.title(title)
  plt.show()

import matplotlib

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

X = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
Y = [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280]
Z = [(6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (5, 2), (4, 2), (5, 2), (3, 2), (1, 1), (3, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (1, 1), (1, 1), (1, 1), (1, 1), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (5, 2), (6, 2), (6, 2), (6, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (6, 2), (6, 2), (6, 2)]
plot(X,Y,Z,"Optimal pooling strategy given number of tests and period for testing","Gap between testing periods","Tests per testing period")
plt.savefig('tests_no_gap'+'.pgf')
#***Optimal pooling strategy given Beta and Gamma***
#Rate of Infection(Beta)
X=[0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.26, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29]
#Rate of Recovery(Gamma)
Y=[0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29, 0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.2, 0.23, 0.26, 0.29]
Z=[(5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (3, 2), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (4, 2), (6, 2), (5, 3), (6, 3), (6, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 2), (6, 2), (6, 2), (5, 2), (4, 2), (6, 3), (6, 3), (5, 3), (5, 3), (5, 3), (1, 1), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 3), (5, 3), (6, 3), (1, 1), (1, 1), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (5, 2), (6, 2), (6, 3), (1, 1), (1, 1), (1, 1), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (1, 1), (1, 1), (1, 1), (1, 1), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (6, 2), (6, 2), (6, 2), (6, 2)]
plot(X,Y,Z,"Optimal pooling strategy given Beta and Gamma","Rate of Infection(Beta)","Rate of Recovery(Gamma) ")
plt.savefig('beta_gamma'+'.pgf')
#***Optimal pooling strategy given Turnaround and Restriction time***
#Test result turnaround time
X=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
#Positive agent restriction time
Y=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Z=[(6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (3, 2), (3, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
plot(X,Y,Z,"Optimal pooling strategy given Turnaround and Restriction time","Test result turnaround time","Positive agent restriction time")
plt.savefig('turnaround_restriction'+'.pgf')
X=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27, 0.27]
Y=[0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27]
Z=[(6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 3), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 3), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (5, 3), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (5, 2), (5, 2), (3, 2), (5, 3), (6, 2), (6, 2), (6, 2), (3, 2), (3, 2), (6, 2), (5, 3), (5, 3), (5, 3), (5, 3), (6, 2), (1, 1), (1, 1), (3, 2), (6, 2), (3, 2), (3, 2), (5, 3), (5, 3), (5, 3), (1, 1), (1, 1), (1, 1), (3, 2), (3, 2), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (1, 1), (1, 1), (1, 1), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3)]
plot(X,Y,Z,"Optimal pooling strategy given False Negative and False Positive rates","False Negative rate","False Positive rate")
plt.savefig('fn_fp'+'.pgf')
#***Optimal pooling strategy given G(n,p) ER random graph***
#Number of agents (n)
X=[1000, 1000, 1000, 1000, 1000, 1000, 1250, 1250, 1250, 1250, 1250, 1250, 1500, 1500, 1500, 1500, 1500, 1500, 1750, 1750, 1750, 1750, 1750, 1750, 2000, 2000, 2000, 2000, 2000, 2000]
#Probability of Edge (p)
Y=[0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035]
Z=[(5, 3), (5, 3), (6, 3), (6, 2), (6, 2), (6, 2), (5, 3), (6, 3), (6, 2), (6, 2), (1, 1), (1, 1), (5, 3), (5, 2), (1, 1), (1, 1), (1, 1), (1, 1), (6, 3), (5, 2), (1, 1), (1, 1), (1, 1), (1, 1), (5, 3), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
plot(X,Y,Z,"Optimal pooling strategy given n and p","Number of agents (n)","Probability of edge (p)")
plt.savefig('np'+'.pgf')
