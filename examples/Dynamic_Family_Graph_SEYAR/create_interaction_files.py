
def create_file(file_name, total, dynamic_num):
    fp = open(file_name,"w")

    if(dynamic_num==1):
        fp.write("<interactions_list1.txt>")
        return

    else:
        str_begin = "<interactions_list"
        str_end = ".txt>\n"

        freq = int(total/dynamic_num)
        print(freq)
        for i in range(dynamic_num):
            num = i+1
            for _ in range(freq):
                fp.write(str_begin+str(num)+str_end)

        rem = total%dynamic_num
        print(rem)
        if(rem!=0):
            for _ in range(rem):
                fp.write(str_begin+str(dynamic_num)+str_end)


# create_file('interaction_files_list1.txt', 50, 1)
# create_file('interaction_files_list2.txt', 50, 2)
# create_file('interaction_files_list3.txt', 50, 3)
# create_file('interaction_files_list4.txt', 50, 4)
# create_file('interaction_files_list5.txt', 50, 5)
# create_file('interaction_files_list6.txt', 50, 6)
# create_file('interaction_files_list7.txt', 50, 7)
# create_file('interaction_files_list8.txt', 50, 8)
# create_file('interaction_files_list9.txt', 50, 9)
# create_file('interaction_files_list10.txt', 50, 10)



create_file('interaction_files_list15.txt', 50, 15)
create_file('interaction_files_list20.txt', 50, 20)
create_file('interaction_files_list25.txt', 50, 25)
create_file('interaction_files_list30.txt', 50, 30)
create_file('interaction_files_list35.txt', 50, 35)
create_file('interaction_files_list40.txt', 50, 40)
create_file('interaction_files_list45.txt', 50, 45)
create_file('interaction_files_list50.txt', 50, 50)
