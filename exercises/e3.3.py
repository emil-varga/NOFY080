import numpy as np

def my_load(filename, comments='#'):
    with open(filename, "r") as file: # open file for reading, with will take care of closing()
        arr = [] #the array of rows
        for line in file: #process file line by line
            #line.strip() removes whitespace (i.e., space and tabs and such) from the
            #beginning and end, then take the first character and compares it with comments
            if line.strip()[0] == comments:
                continue # if it matches, skip the line
            # otherwise convert the text to numbers
            #line.split() splits the string to a list of substrings separated by whitespace, i.e.
            #"aaa bbb ccc".split() = ["aaa", "bbb", "ccc"]
            row = [float(tok) for tok in line.split()] # construct the row using list comprehension (see below)
            arr.append(row) # save the row
        return np.array(arr) #convert everything to 2D array and return
    
print(my_load("data.txt"))

### LIST COMPREHENSION
#[operation(x) for x in iterable]
#is roughly equivalent to:
#lst = []
#for x in iterable:
#    lst.append(operation(x))