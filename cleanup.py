import os
import time
import datetime
import csv
output_list = []
rootdir = 'clean_gram'
lookup = {}


def store_location_of_where_we_start_looking():
    for subdirz in os.walk(rootdir):
        for sub in subdirz[1]:
            if "2016" in sub:
                start_timestamp = convert_to_unix_timestamp(sub)
                i = binary_search(start_timestamp, 0, len(output_list) - 1)
                lookup[sub] = i


def binary_search( start_timestamp, low, high):
    if high >= low:
        mid = (high + low) // 2
        end_timestamp = start_timestamp + (5 * 60 * 60)
        if start_timestamp <= int(output_list[mid][0]) <= end_timestamp:
            return mid
        elif int(output_list[mid][0]) > start_timestamp:
            return binary_search(start_timestamp, low, mid - 1)
        else:
            return binary_search(start_timestamp, mid + 1, high)

    else:
        return -1


def convert_to_unix_timestamp(date):
    # if "-2" in date:
    #     date = date.replace("-2","")
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())


def read_input():
    for i in range(1):
        f = open("edges2016Outputs/outputs2016_{0}.txt".format(i+1), "r")
        for x in f:
            line = x.strip("\n")
            output_list.append(line.split("\t"))
        # with open("edges2016Outputs/outputs2016_{0}.txt".format(i + 1), "r") as csv_filea:
        #     csv_readera = csv.reader(csv_filea)
        #     for rowa in csv_readera:
        #         print(rowa)
        #         output_list.append(rowa[0].split("\t"))
        # dask_df = dd.read_csv("edges2016Outputs/outputs2016_{0}.txt".format(i + 1))


read_input()

store_location_of_where_we_start_looking()
print(lookup)
for subdir, dirs, files in os.walk(rootdir):
    sub = subdir.replace("clean_gram\\", "")
    os.mkdir('results/{0}'.format(sub))
    for file in files:
        line_count = 0
        if "2016" in subdir:
            print(os.path.join(subdir, file))
            with open(os.path.join(subdir, file), mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                with open("results/{0}/{1}".format(sub, file), "a", newline='') as csv_w_file:
                    fieldnames = ["vendor_name", "price", "name", "description", "add_time", "ship_from", "addresses", "number_of_addresses", "number_of_outputs"]
                    writer = csv.DictWriter(csv_w_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in csv_reader:
                        amount_of_transaction_found = 0
                        addresses_found = []
                        n_of_addresses = 0
                        if float(row["price"]) != 0:
                            index = lookup[subdir.replace("clean_gram\\", "")]
                            price_in_satoshi = str(round(float(row["price"]) * 10 ** 8))
                            stop = (convert_to_unix_timestamp(subdir.replace("clean_gram\\",  "")) + (1440 * (60**2))) # look for two months

                            while int(output_list[index][0]) < stop:
                                if price_in_satoshi in output_list[index]:
                                    last_index = len(output_list[index]) - 2
                                    n_of_addresses = int(last_index / 2)
                                    amount_of_transaction_found += 1
                                    addresses_found.append(output_list[index][output_list[index].index(price_in_satoshi) - 1])
                                index += 1
                        row["addresses"] = addresses_found
                        row["number_of_addresses"] = amount_of_transaction_found
                        row["number_of_outputs"] = n_of_addresses
                        writer.writerow(row)




