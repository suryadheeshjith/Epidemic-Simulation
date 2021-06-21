# Usage : python3 Print_optimal.py <csv file> <test_cost> <fp_cost> <quarantine_cost> <infection_cost>

import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
k = 1
def plot(X,Y,Z,title='',xlabl='',ylabl=''):
  global k
  color_list={(1,1):'cyan',(2,1):'blue',(3,2):'green',(4,2):'pink',(5,2):'orange',(5,3):'red',(6,2):'purple',(6,3):'grey'}
  # fig,ax=plt.subplots()
  plt.subplot(2, 3, k)
  k+=1
  for i in range(len(X)):
    plt.scatter(X[i],Y[i],color=color_list[Z[i]],s=20,alpha=0.8,edgecolors='none')
  #ax.legend(color_list.keys())
  #ax.grid(True)
  plt.xlabel(xlabl)
  plt.ylabel(ylabl)
  plt.title(title)

def print_optimal_rows(file_name, a,b):
    test_cost = int(sys.argv[1])
    fp_cost = int(sys.argv[2])
    quarantine_cost = int(sys.argv[3])
    infection_cost = int(sys.argv[4])
    num_pool_strats = 8
    X = []
    Y = []
    Z = []

    with open(file_name, mode = 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        opt_cost=np.inf
        opt_pool=None
        ls = []
        file_p = open("cost_csv.txt","w")
        file_p.write("beta \t gamma \t n \t\t\t p \t testing_gap \t tests_per_period \t turnaround_time \t restriction_time \t fn \t fp \t Optimal \t\t Costs\n")
        for i,dict in enumerate(csv_reader):
            cost = infection_cost*float(dict['total_infection']) + quarantine_cost*float(dict['total_quarantined_days']) + test_cost*float(dict['total_test_cost']) + fp_cost*float(dict['total_false_positives'])
            print(dict['napt'],dict['ntpa'],cost)
            ls.append(cost)
            if cost < opt_cost:
                opt_cost= cost
                opt_pool=(int(dict['napt']),int(dict['ntpa']))
            if((i+1) % num_pool_strats==0):
                ls = np.sort(ls)
                file_p.write("{0} \t\t {1} \t {2} \t {3} \t\t\t {4} \t\t\t\t {5} \t\t\t\t\t\t\t\t {6} \t\t\t\t\t\t\t {7} \t\t\t\t\t\t\t {8} \t\t\t {9} \t\t\t\t {10}  \t\t\t\t {11}\n".format(dict['beta'],dict['gamma'],dict['n'],dict['p'],dict['testing_gap'],dict['tests_per_period'],dict['turnaround_time'],dict['restriction_time'],dict['fn'],dict['fp'],opt_pool,ls))
                X.append(dict[a])
                Y.append(dict[b])
                Z.append(opt_pool)
                opt_cost=np.inf
                opt_pool=None
                ls = []

    return X, Y, Z


# Beta, gamma
X,Y,Z = print_optimal_rows('beta_gamma.csv','beta','gamma')
plot(X,Y,Z,"Optimal pooling strategy given Beta and Gamma","Rate of Infection(Beta)","Rate of Recovery(Gamma) ")

# fn, fp
X,Y,Z = print_optimal_rows('fn_fp.csv','fn','fp')
plot(X,Y,Z,"Optimal pooling strategy given False Negative and False Positive rates","False Negative rate","False Positive rate")

# Turnaround time, restriction time
X,Y,Z = print_optimal_rows('turnaround_time_19_Jun.csv','turnaround_time','restriction_time')
plot(X,Y,Z,"Optimal pooling strategy given Turnaround and Restriction time","Test result turnaround time","Positive agent restriction time")

# n, p
X,Y,Z = print_optimal_rows('np.csv','n','p')
plot(X,Y,Z,"Optimal pooling strategy given n and p","Number of agents (n)","Probability of edge (p)")


# Gap tests, tests_per_period
X,Y,Z = print_optimal_rows('gap_tests_20_Jun.csv','testing_gap','tests_per_period')
plot(X,Y,Z,"Optimal pooling strategy given number of tests and period for testing","Gap between testing periods","Tests per testing period")

plt.show()
