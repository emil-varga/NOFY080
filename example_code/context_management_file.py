import numpy as np

class MyNumpyFile:
    def __init__(self, filename, mode='w'):
        print("Opening file.")
        self.file = open(filename, mode)
    
    def write(self, data):
        np.savetxt(self.file, data)

    def __enter__(self):
        print("Entering with statement")
        return self
    def __exit__(self, *exc):
        print("Closing.")
        self.file.close()

print("I'm about to open the file.")
with MyNumpyFile("my_array.txt", 'w') as file:
    file.write(np.arange(5))
print("The end.")