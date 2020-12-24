# AdversarialMatching

# Abstract 
Trading on the darknet market provides privacy for both vendors and consumers looking to buy and sell illegal items. 
The idea of anonymity which is achieved using The Onion Router(TOR), an encrypted network, has brought about
tremendous growth to the market as vendors and consumers alike feel protected from agencies that might take interest 
in tracing them. This paper takes an in-depth look into the products sold on the network and also analyzes the seller 
on the darknet marketplace. In addition, we propose and design a system that performs single and multi market analysis.
In single market analysis, we identify all the addresses that can possibly belong to a vendor, while in multi market
analysis, we try to probabilistically match users across multi market darknet marketplaces.

# single_market_analysis.py

This script helps us perform single market analysis. 
it maps the  output file structure to mimic the input gram file structure.
it creates all the subdirectories and inside those directories the marketplace 
darknet files. The output file each contains the the "vendor name", "name", "description", 
"number_of_addresses","addresses","number_of_outputs". 
We search for transactions from a start time which is the name of the subdirectory and the endtime 
which is one day plus the start time. Since the output edge data is sorted by time we used that fact to 
binary search for the start time in the list of outputs and find the transaction that is closest to that
unix time. 

# duplicate_removal.py

this code creates a new directory that matches the grams dataset, it remove all the duplicate between files
of the same marketplace. 

# remove_column.py

this code creates a new directory that matches the grams dataset, it removes all the columns specified
