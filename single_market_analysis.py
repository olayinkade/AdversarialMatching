import os
import time
import datetime
import csv
output_list = []
root_dir = 'clean_gram'
lookup = {}

curr_year = "2016"


# This function stores where to start searching for a specific product by looking at the date of the subdirectory
# and  comparing it to the output edge file
def store_location_of_where_we_start_looking(m):
    month_year = curr_year + "-{0:02d}".format(m)
    for subdirz in os.walk(root_dir):
        for sub in subdirz[1]:
            if month_year in sub:
                start_timestamp = convert_to_unix_timestamp(sub)
                curr__item_index = binary_search(start_timestamp, 0, len(output_list) - 1)
                lookup[sub] = curr__item_index


# searches for a date closest to that in the subdirectory directory
# in the output edge file.
def binary_search(start_timestamp, low, high):
    if high >= low:
        mid = (high + low) // 2
        end_timestamp = start_timestamp + (5 * 60 * 60)  # looking for a valid stamp in the five hour range
        if start_timestamp <= int(output_list[mid][0]) <= end_timestamp:
            return mid
        elif int(output_list[mid][0]) > start_timestamp:
            return binary_search(start_timestamp, low, mid - 1)
        else:
            return binary_search(start_timestamp, mid + 1, high)
    else:
        return -1


def convert_to_unix_timestamp(date):
    if date.endswith("-2"):
        date = date.replace("-2", "")
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())


# This function opens a respective output edge file
def read_input(value):
    f = open("edges"+curr_year+"Outputs/outputs"+curr_year+"_{0}.txt".format(value), "r")
    for x in f:
        line = x.strip("\n")
        output_list.append(line.split("\t"))
    return f


def processor():
    curr_month = 1
    curr_f = read_input(curr_month)

    store_location_of_where_we_start_looking(curr_month)
    print(lookup)
    os.mkdir('results')

    for subdir, dirs, files in os.walk(root_dir):
        sub = subdir.replace("clean_gram\\", "")
        if "clean_gram" not in sub:
            os.mkdir('results/{0}'.format(sub))

    for subdir, dirs, files in os.walk(root_dir):
        sub = subdir.replace("clean_gram\\", "")
        for file in files:
            if curr_year in subdir:
                month = subdir.split("-")[1]
                if int(month) > curr_month:
                    curr_f.close()
                    curr_month += 1
                    read_input(curr_month)
                    store_location_of_where_we_start_looking(curr_month)
                print(os.path.join(subdir, file))
                with open(os.path.join(subdir, file), mode='r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    with open("results/{0}/{1}".format(sub, file), "a", newline='') as csv_w_file:
                        fieldnames = ["vendor_name", "price", "name", "description", "add_time", "ship_from", "addresses",
                                      "number_of_addresses", "number_of_outputs"]
                        writer = csv.DictWriter(csv_w_file, fieldnames=fieldnames)
                        writer.writeheader()
                        for row in csv_reader:
                            amount_of_transaction_found = 0
                            addresses_found = []
                            n_of_addresses = 0
                            if float(row["price"]) != 0:
                                index = lookup[subdir.replace("clean_gram\\", "")]
                                price_in_satoshi = round(float(row["price"]) * 10 ** 8)
                                stop = (convert_to_unix_timestamp(subdir.replace("clean_gram\\",  "")) + (24 * (60**2)))
                                if index != -1:
                                    while int(output_list[index][0]) < stop:
                                        # if price_in_satoshi in output_list[index]:
                                        last_index = len(output_list[index]) - 2
                                        n_of_addresses = int(last_index / 2)
                                        curr_value = 3
                                        for i in range(n_of_addresses):
                                            if int(output_list[index][curr_value]) != 0 and int(output_list[index][curr_value]) % price_in_satoshi == 0:
                                                amount_of_transaction_found += 1
                                                addresses_found.append(output_list[index][curr_value-1])

                                            curr_value += 2
                                        index += 1
                            row["addresses"] = addresses_found
                            row["number_of_addresses"] = amount_of_transaction_found
                            if amount_of_transaction_found != 0:
                                row["number_of_outputs"] = n_of_addresses
                                writer.writerow(row)
                    csv_w_file.close()
                csv_file.close()


processor()