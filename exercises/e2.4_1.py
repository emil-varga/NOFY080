Nstr = input("Number of names:")
#input always_ returns a string, we need to explicitly convert 
N = int(Nstr) #equivalently, N = int(input("number of names:"))

#we need a place to save the names, we'll use a list
names = [] #start with empty

#underscore is a variable name which conventionally mean
#that we don't care about the value. We only need that the
#loop runs N times
for _ in range(N):
    name = input("Enter a name: ")
    # we always append the name to the end, that's why
    # we don't need the iteration idnex
    names.append(name) 
#now the loop contains N strings

#everyting in python is an object, object have methods which work
#with the specific data that the object represent (we'll see OOP later)

#list supports a sort() method, which sorts the contents of the list
names.sort()

#and now we can pring
for name in names:
    print(name)
