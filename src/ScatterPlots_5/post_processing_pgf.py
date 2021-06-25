import numpy as np
import sys
import csv
import copy
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
# })

k=1
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
            # print(dict['napt'],dict['ntpa'],cost)
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

def plot(X,Y,Z,title='',xlabl='',ylabl='',fname='', leg = False):
    if(not leg):
        for i in range(len(X)):
            plt.scatter(X[i],Y[i],color=Z[0][i],s=20,alpha=0.8,edgecolors='none')
        plt.xlabel(xlabl)
        plt.ylabel(ylabl)
        plt.title(title)
        # plt.savefig('fig_{0}.pgf'.format(fname))

        plt.show()
        plt.clf()
    else:
        plt.subplot(1, 3, 1)
        for i in range(len(X)):
            plt.scatter(X[i],Y[i],color=Z[0][i],s=20,alpha=0.8,edgecolors='none')
        plt.xlabel(xlabl)
        plt.ylabel(ylabl)
        plt.title(title)
        # fig,ax=plt.subplots()
        plt.subplot(1, 3, 3)
        color_list={(1,1):'cyan',(2,1):'blue',(3,2):'grey',(4,2):'pink',(5,2):'orange',(5,3):'red',(6,2):'purple',(6,3):'green'}
        points=[]
        for c in color_list.keys():
            points.append(plt.scatter(0,0,color=color_list[c],s=20,alpha=0.8,edgecolors='none'))
        plt.subplot(1, 3, 2)
        legendFig = plt.figure("Legend plot")
        legendFig.legend(points, color_list.keys(), loc='center', prop={'size': 13})
        plt.show()

def frame(mat):
    out_mat = []
    for i in range(len(mat)+2):
        temp = []
        for j in range(len(mat[0])+2):
            temp.append('0')
        out_mat.append(temp)

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            out_mat[i+1][j+1] = mat[i][j]

    return out_mat

def find_max_occurence(color, ls):
    if(color in ls):
        return color
    d = {}
    for i in ls:
        try:
            d[i]+=1
        except:
            d[i]=1
    max = 0
    max_col = None
    for key in d.keys():
        if(d[key]>max):
            max_col = key
            max = d[key]
    # print(ls,max_col)
    return max_col

def find_true_col(i, j, mat_framed):
    i+=1
    j+=1
    x = [-1,0,1]
    y = [-1,0,1]
    ls = []
    for x_ in x:
        for y_ in y:
            if mat_framed[i+x_][j+y_] != '0':
                if(not (x_==0 and y_==0)):
                    ls.append(mat_framed[i+x_][j+y_])
    # print(i,j)
    return find_max_occurence(mat_framed[i][j], ls)


def convert_1d_to_2d(ls, i, j):
    return np.reshape(np.array(ls), (i, j))

def convert_2d_to_1d(mat):
    return np.reshape(np.array(mat),(1,-1))

def clean(ls, k, l):
    color_list={(1,1):'cyan',(2,1):'blue',(3,2):'grey',(4,2):'pink',(5,2):'orange',(5,3):'red',(6,2):'purple',(6,3):'green'}
    for i in range(len(ls)):
        ls[i] = color_list[ls[i]]
    # print(ls)
    mat = convert_1d_to_2d(ls, k, l)
    # print(mat)

    new_mat = copy.deepcopy(mat)
    mat_framed = frame(mat)
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            new_mat[i][j] = find_true_col(i,j,mat_framed)

    # print(new_mat)

    return convert_2d_to_1d(new_mat)


# Beta, gamma
# X,Y,Z = print_optimal_rows('beta_gamma_90_100.csv','beta','gamma')
# plot(X,Y,clean(Z, 9, 10),"Optimal pooling strategy given Beta and Gamma","Rate of Infection(Beta)","Rate of Recovery(Gamma) ", "beta_gamma")
#
# # fn, fp
# X,Y,Z = print_optimal_rows('fn_fp.csv','fn','fp')
# plot(X,Y,clean(Z, 9, 10),"Optimal pooling strategy given False Negative and False Positive rates","False Negative rate","False Positive rate", "fn_fp")
# #
# # # # n, p
# X,Y,Z = print_optimal_rows('np.csv','n','p')
# plot(X,Y,clean(Z, 5, 6),"Optimal pooling strategy given n and p","Number of agents (n)","Probability of edge (p)","np")
# #
# #
# # # Gap tests, tests_per_period
# X,Y,Z = print_optimal_rows('gap_tests.csv','testing_gap','tests_per_period')
# plot(X,Y,clean(Z, 5, 10),"Optimal pooling strategy given number of tests and period for testing","Gap between testing periods","Tests per testing period","gap_tests")


# Turnaround time, restriction time
X,Y,Z = print_optimal_rows('turnaround_restriction_90_100.csv','turnaround_time','restriction_time')
plot(X,Y,clean(Z, 5, 10),"Optimal pooling strategy given Turnaround and Restriction time","Test result turnaround time","Positive agent restriction time","turnaround_restriction", True)

#
# plt.show()
