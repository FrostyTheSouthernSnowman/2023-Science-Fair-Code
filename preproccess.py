# import the csv module
import csv
# import the tqdm module
from tqdm import tqdm

# open the original file in read mode
with open("7.4V_output.csv", "r") as infile:
    # create a csv reader object
    reader = csv.reader(infile)
    # open a temporary file in write mode
    with open("temp.csv", "w") as outfile:
        # create a csv writer object
        writer = csv.writer(outfile)
        # initialize a counter variable
        counter = 0
        # loop through the rows in the original file with a tqdm progress bar
        for row in tqdm(reader):
            # increment the counter
            counter += 1
            # check if the counter is divisible by 1000
            if counter % 100 == 1:
                # write the row to the temporary file
                writer.writerow(row)
# import the os module
import os

os.rename("7.4V_output.csv", "7.4V_original_output.csv")
# rename the temporary file as the original file
os.rename("temp.csv", "7.4V_output.csv")
# print the completion message
print("Finished processing the file")
