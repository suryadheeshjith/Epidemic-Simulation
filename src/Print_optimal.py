# Usage : python3 Print_optimal.py <csv file> <test_cost> <fp_cost> <quarantine_cost> <infection_cost>

import csv
import sys
import numpy as np

def print_optimal_rows():
    file_name = sys.argv[1]
    test_cost = int(sys.argv[2])
    fp_cost = int(sys.argv[3])
    quarantine_cost = int(sys.argv[4])
    infection_cost = int(sys.argv[5])
    num_pool_strats = 8

    with open(file_name, mode = 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        opt_cost=np.inf
        opt_pool=None
        file_p = open("cost_csv.txt","w")
        file_p.write("beta \t gamma \t n \t\t\t p \t testing_gap \t tests_per_period \t turnaround_time \t restriction_time \t fn \t fp \t Optimal \n")
        for i,dict in enumerate(csv_reader):
            cost = infection_cost*float(dict['total_infection']) + quarantine_cost*float(dict['total_quarantined_days']) + test_cost*float(dict['total_test_cost']) + fp_cost*float(dict['total_false_positives'])
            print(dict['napt'],dict['ntpa'],cost)
            if cost < opt_cost:
                opt_cost= cost
                opt_pool=(dict['napt'],dict['ntpa'])
            if((i+1) % num_pool_strats==0):
                file_p.write("{0} \t\t {1} \t {2} \t {3} \t\t\t {4} \t\t\t\t {5} \t\t\t\t\t\t\t\t {6} \t\t\t\t\t\t\t {7} \t\t\t\t\t\t\t {8} \t\t\t {9} \t\t\t\t {10}\n".format(dict['beta'],dict['gamma'],dict['n'],dict['p'],dict['testing_gap'],dict['tests_per_period'],dict['turnaround_time'],dict['restriction_time'],dict['fn'],dict['fp'],opt_pool))
                opt_cost=np.inf
                opt_pool=None



print_optimal_rows()
