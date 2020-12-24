# Given a file name, this program goes through all the files in the directory and removes duplicates.
import os
import csv
from shutil import copy

files_in_dir = {'ADM.csv', 'Haven.csv', 'Oasis.csv', 'Tochka.csv', 'TPM.csv', 'Pandora.csv', 'TOM.csv', 'OutLaw.csv',
 'EVO2.csv', 'NK.csv', 'Abraxas.csv', 'Dream.csv', 'Alpha.csv', 'RealDeal.csv', '1776.csv', 'SilkRoad.csv',
 'Silkkitie.csv', 'Bungee54.csv', 'EVO.csv', 'BB.csv', 'Hansa.csv', 'Oxygen .csv', 'Alpaca.csv', 'Valhalla.csv',
'C9.csv', 'ME.csv', 'Agora.csv'}
root_dir = 'clean_gram'
fieldnames = ["vendor_name", "price", "name", "description", "add_time", "ship_from"]


def retrieve_file():
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            files_in_dir.add(file)
    print(files_in_dir)


retrieve_file()


def processor():
    similar_transaction = 0
    os.mkdir('duplicate')

    for subdir, dirs, files in os.walk(root_dir): # matches directory of  clean gram dataset
        sub = subdir.replace("clean_gram\\", "")
        if "clean_gram" not in sub:
            os.mkdir('duplicate/{0}'.format(sub))

    for item in files_in_dir: # find all path to files that in the directory
        curr_files = []
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if item in file:
                    curr_files.append(os.path.join(subdir, file))
        # compares two files and the content in them

        dirs = (curr_files[0].replace("clean_gram\\", "")).split("\\")
        copy(curr_files[0], 'duplicate/{0}'.format(dirs[0]))
        for i in range(len(curr_files)):
            print(curr_files[i])
            with open('duplicate/{0}'.format(curr_files[i].replace("clean_gram\\", "")), mode='r') as csv_file1:
                csv_reader = csv.DictReader(csv_file1)
                for j in range(i+1, len(curr_files)):
                    print(i, j)
                    with open(curr_files[j], mode='r') as csv_file2:
                        csv_reader2 = csv.DictReader(csv_file2)
                        sub = curr_files[j].replace("clean_gram\\", "")
                        with open("duplicate/{0}".format(sub), "w", newline='') as csv_w_file:
                            writer = csv.DictWriter(csv_w_file, fieldnames=fieldnames)
                            writer.writeheader()
                            found = False
                            for row in csv_reader2:
                                for rowa in csv_reader:
                                    column_name = ["vendor_name", "price", "name", "description", "ship_from"]
                                    for obj in column_name:  # compares two rows and check if they are the same by  comparing all the columns
                                        if row[obj] == rowa[obj]:
                                            found = True
                                        elif row[obj] != rowa[obj]:
                                            found = False
                                            break
                                    if found:
                                        break
                                csv_file1.seek(0)  # make sure that we are restarting the row, so it starts from the top
                                csv_reader = csv.DictReader(csv_file1)
                                if found:
                                    print(row)
                                    similar_transaction += 1
                                else:
                                    writer.writerow(row)
                        csv_file1.seek(0)
                        csv_reader = csv.DictReader(csv_file1)

        print(similar_transaction)


processor()

