import os
import csv

# the directory that houses the csv files
dir_name = "/home/cfsl/Documents/cleanGram/clean_gram"

os.mkdir('new_sub2')

#for creating a clone of the directory that houses the csv comparison results
for direc, subdir, files in os.walk(dir_name):
    for sub_d in subdir:
        os.mkdir('new_sub2/{0}'.format(sub_d))



duplicate_count = 0
curr_file = []
for subdir in os.walk(dir_name):
    for sub in subdir[1]:
        for direc, sub_d, filenames in os.walk(os.path.join(dir_name,sub)):
            for files in filenames:
                
                curr_file.append(os.path.join(sub,files)) #creating a list that houses the csv files we will use in comparison
            
            # opening the first csv file and reading it
            for i in range(len(curr_file)):
                with open(os.path.join(dir_name,curr_file[i]), "r") as first_csv_file:
                    first_csv_reader = csv.DictReader(first_csv_file)
                    
                    # opening the second csv file for comparison with the first csv file
                    for j in range(i+1,len(curr_file)):
                        
                        with open(os.path.join(dir_name,curr_file[j]), "r") as second_csv_file:
                            second_csv_reader = csv.DictReader(second_csv_file)
                            curr_r = (curr_file[i].split("/")[1]).split(".")[0] + curr_file[j].split("/")[1]
                            with open("new_sub2/{0}".format(os.path.join(curr_file[i].split("/")[0],curr_r)), "w", newline='') as write_file:
                                fieldnames = ["vendor_name","price","name","description", "add_time","ship_from"]
                                write_new_csv = csv.DictWriter(write_file, fieldnames= fieldnames)

                                write_new_csv.writeheader()
                                duplicate_found = False
                                #comparing the variables to check for similarities 
                                for first_row_one in first_csv_reader:
                                    for first_row_two in second_csv_reader:
                        
                                        col_name = ["vendor_name","name","description","ship_from"]
                                        for col in col_name:
                                            if first_row_two[col] == first_row_one[col]:
                                                duplicate_found = True
                                            else:
                                                duplicate_found = False
                                                break
                                        if duplicate_found:
                
                                            break
                                    first_csv_file.seek(0)
                                    first_csv_reader = csv.DictReader(first_csv_file)
                                    if duplicate_found:
                                        #writing outcome to file 
                                        duplicate_count += 1
                                        write_new_csv.writerow(first_row_one)
                                    else:
                                        break
                                first_csv_file.seek(0)
                                first_csv_reader = csv.DictReader(first_csv_file)    
                                print(duplicate_count)

            curr_file =[]