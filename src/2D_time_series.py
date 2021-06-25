import sys
import ReadFile
import pickle
import World
import importlib.util
import os.path as osp
import policy_generator as pg
import matplotlib
import matplotlib.pyplot as plt
'''
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})'''
import numpy as np

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_example_path():
    return sys.argv[1]


def get_config_path(path):
    config_filepath=osp.join(path,'config.txt')
    return config_filepath


def get_file_paths(example_path,config_obj):
    # File Names
    locations_filename=None
    agents_filename=osp.join(example_path,config_obj.agents_filename)
    interactions_FilesList_filename=osp.join(example_path,config_obj.interactions_files_list)
    events_FilesList_filename=osp.join(example_path,config_obj.events_files_list)
    if config_obj.locations_filename=="":
        locations_filename=None
    else:
        locations_filename=osp.join(example_path,config_obj.locations_filename)

    return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename


def get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj):
    # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

    interactions_files_list=None
    events_files_list=None

    if config_obj.interactions_files_list=='':
        print('No Interaction files uploaded!')
    else:
        interactionFiles_obj=ReadFile.ReadFilesList(interactions_FilesList_filename)
        interactions_files_list=list(map(lambda x : osp.join(example_path,x) ,interactionFiles_obj.file_list))
        if interactions_files_list==[]:
            print('No Interactions inputted')


    if config_obj.events_files_list=='':
        print('No Event files uploaded!')
    else:
        eventFiles_obj=ReadFile.ReadFilesList(events_FilesList_filename)
        events_files_list=list(map(lambda x : osp.join(example_path,x) ,eventFiles_obj.file_list))
        if events_files_list==[]:
            print('No Events inputted')

    return interactions_files_list, events_files_list

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn

if __name__=="__main__":

    example_path = get_example_path()
    config_filename = get_config_path(example_path)

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
    events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
    interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

    # User Model
    model = get_model(example_path)

    ##########################################################################################

    fp = open("2D_time_series.txt","w")
    num_tests = 90
    pools_list = [(None,None),(1,1),(2,1),(3,2)]
    tdicts = []
    for i,j in pools_list:
        if(i and j):
            policy_list, event_restriction_fn =  pg.generate_group_testing_tests_policy(num_tests, i, j)
        else:
            policy_list, event_restriction_fn =  pg.generate_no_policy()

        world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
        tdict, total_infection, total_quarantined_days, wrongly_quarantined_days, total_test_cost = world_obj.simulate_worlds(plot=False)
        fp.write("("+str(i)+","+str(j)+") : ")
        fp.write(str(tdict)+"\n")
        tdicts.append(tdict)

    fp.close()
    # Plots
    # tdicts = [{'Susceptible': [970.0, 953.26, 929.44, 897.7, 852.74, 795.54, 723.9, 639.7, 547.08, 455.98, 368.5, 291.38, 225.9, 176.36, 137.46, 107.98, 87.26, 71.86, 60.54, 51.64, 43.88, 39.04, 35.2, 32.12, 29.8, 27.6, 26.02, 24.68, 23.82, 23.1, 22.24], 'Infected': [30.0, 43.12, 61.62, 85.82, 120.44, 163.84, 215.2, 273.3, 331.52, 382.92, 423.84, 450.76, 463.26, 457.98, 440.68, 417.96, 387.4, 354.22, 323.4, 293.68, 266.86, 239.0, 213.6, 191.58, 170.78, 152.32, 134.84, 119.66, 106.16, 94.0, 82.86], 'Recovered': [0.0, 3.62, 8.94, 16.48, 26.82, 40.62, 60.9, 87.0, 121.4, 161.1, 207.66, 257.86, 310.84, 365.66, 421.86, 474.06, 525.34, 573.92, 616.06, 654.68, 689.26, 721.96, 751.2, 776.3, 799.42, 820.08, 839.14, 855.66, 870.02, 882.9, 894.9]},{'Susceptible': [970.0, 954.0, 933.38, 908.72, 878.36, 842.72, 799.7, 750.6, 697.16, 639.9, 581.4, 522.48, 467.6, 418.08, 371.68, 330.46, 295.74, 265.96, 240.82, 219.9, 202.26, 187.92, 175.78, 166.52, 158.02, 150.66, 145.38, 140.36, 135.62, 131.84, 128.52], 'Infected': [30.0, 42.2, 58.16, 76.02, 96.84, 121.08, 149.76, 180.58, 212.28, 244.62, 274.1, 300.94, 320.6, 331.44, 338.14, 337.2, 333.26, 322.4, 307.8, 290.42, 274.44, 256.24, 238.5, 218.14, 200.84, 183.74, 167.22, 151.7, 139.52, 126.94, 114.86], 'Recovered': [0.0, 3.8, 8.46, 15.26, 24.8, 36.2, 50.54, 68.82, 90.56, 115.48, 144.5, 176.58, 211.8, 250.48, 290.18, 332.34, 371.0, 411.64, 451.38, 489.68, 523.3, 555.84, 585.72, 615.34, 641.14, 665.6, 687.4, 707.94, 724.86, 741.22, 756.62]},{'Susceptible': [970.0, 956.54, 941.86, 925.76, 907.92, 888.76, 868.96, 848.04, 827.22, 806.34, 785.12, 765.22, 744.72, 725.56, 706.9, 688.32, 671.86, 656.5, 641.14, 626.86, 613.46, 600.74, 588.74, 577.86, 567.52, 558.4, 550.36, 542.3, 535.08, 528.04, 521.26], 'Infected': [30.0, 40.06, 50.28, 60.44, 71.24, 81.94, 92.32, 102.38, 111.48, 118.9, 125.58, 130.46, 135.64, 139.0, 140.88, 142.5, 142.62, 141.12, 139.58, 137.3, 134.28, 131.02, 127.5, 122.58, 117.28, 113.0, 107.78, 102.8, 97.7, 93.24, 89.04], 'Recovered': [0.0, 3.4, 7.86, 13.8, 20.84, 29.3, 38.72, 49.58, 61.3, 74.76, 89.3, 104.32, 119.64, 135.44, 152.22, 169.18, 185.52, 202.38, 219.28, 235.84, 252.26, 268.24, 283.76, 299.56, 315.2, 328.6, 341.86, 354.9, 367.22, 378.72, 389.7]},{'Susceptible': [970.0, 955.96, 939.48, 918.86, 893.96, 865.76, 835.18, 800.32, 763.66, 726.24, 688.0, 651.86, 614.92, 581.24, 550.14, 520.48, 493.54, 470.04, 448.36, 428.7, 412.14, 397.42, 384.34, 372.94, 362.94, 354.22, 346.26, 338.34, 331.5, 325.0, 319.18], 'Infected': [30.0, 40.48, 52.34, 66.54, 83.64, 101.92, 121.56, 141.88, 161.48, 178.7, 194.94, 207.06, 219.24, 226.86, 231.16, 232.2, 231.84, 227.32, 222.66, 215.52, 207.62, 196.82, 185.78, 176.02, 165.7, 154.6, 145.22, 135.34, 126.72, 118.48, 108.98], 'Recovered': [0.0, 3.56, 8.18, 14.6, 22.4, 32.32, 43.26, 57.8, 74.86, 95.06, 117.06, 141.08, 165.84, 191.9, 218.7, 247.32, 274.62, 302.64, 328.98, 355.78, 380.24, 405.76, 429.88, 451.04, 471.36, 491.18, 508.52, 526.32, 541.78, 556.52, 571.84]}]

    fig,a =  plt.subplots(2,2)
    for indx,(i,j) in enumerate(pools_list):
        if(indx==0):
            plotter = a[0][0]
        elif(indx==1):
            plotter = a[0][1]
        elif(indx==2):
            plotter = a[1][0]
        elif(indx==3):
            plotter = a[1][1]

        for state in tdicts[0].keys():
            plotter.plot(tdicts[indx][state])
        if(i and j):
           plotter.set_title("Testing with (napt,ntpa) = ({0},{1})".format(i,j))
        else:
            plotter.set_title("No Testing")
        plotter.legend(list(tdicts[0].keys()),loc='upper right', shadow=True)

    plt.show()
    #plt.savefig('2D_time_series.pgf')

    ###############################################################################################
