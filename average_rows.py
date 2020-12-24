# Given a file name, this program goes through all the files in the directory and removes duplicates.
import os
import csv
files_in_dir = {'ADM.csv', 'Haven.csv', 'Oasis.csv', 'Tochka.csv', 'TPM.csv', 'Pandora.csv', 'TOM.csv', 'OutLaw.csv',
 'EVO2.csv', 'NK.csv', 'Abraxas.csv', 'Dream.csv', 'Alpha.csv', 'RealDeal.csv', '1776.csv', 'SilkRoad.csv',
 'Silkkitie.csv', 'Bungee54.csv', 'EVO.csv', 'BB.csv', 'Hansa.csv', 'Oxygen .csv', 'Alpaca.csv', 'Valhalla.csv',
'C9.csv', 'ME.csv', 'Agora.csv'}


root_dir = 'clean_gram3'
fieldnames = ["vendor_name", "price", "name", "description", "add_time", "ship_from"]


def processor():
    total = 0
    for item in files_in_dir: # find all path to files that in the directory
        curr_files = []
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if item in file:

                        curr_files.append(os.path.join(subdir, file))
        # compares two files and the content in them

        for i in range(len(curr_files)):
            print(curr_files[i])
            with open(root_dir + '/{0}'.format(curr_files[i].replace(root_dir+"\\", "")), mode='r') as csv_file1:
                csv_reader = csv.DictReader(csv_file1)

                for rowa in csv_reader:
                    total = total + 1
        print(total/len(curr_files))


processor()

