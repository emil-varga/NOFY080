#we need a place to save the names, we'll use a list
names = [] #start with empty

#we run forever
while True:
    name = input("Enter a name: ")
    if name == "":
        break #end if name is empty string
    # append at the otherwise
    names.append(name) 

names.sort()

#and now we can print
for name in names:
    #<e2.3_3>
    if name.upper() == 'EMIL':
        continue
    #</e2.3_3>
    print(name)
