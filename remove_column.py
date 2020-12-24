import os
import csv

output_list = []
rootdir = 'grams'
lookup = {}


for subdir, dirs, files in os.walk(rootdir):
    sub = subdir.replace("grams\\", "")

    os.mkdir('clean2_gram/{0}'.format(sub))
    for file in files:
        with open(os.path.join(subdir, file), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open("clean2_gram/{0}/{1}".format(sub, file), "a", newline='') as csv_w_file:
                fieldnames = ["vendor_name", "price", "name", "description", "add_time", "ship_from"]
                writer = csv.DictWriter(csv_w_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in csv_reader:
                    if row["price"] != 0:
                        if None in row.keys():
                            row[None] = ""
                            del row[None]

                        keys_to_remove = ["hash", "item_link", "image_link", "market_name", ""]
                        for key in keys_to_remove:
                            del row[key]

                        writer.writerow(row)












