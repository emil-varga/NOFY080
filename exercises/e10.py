import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('data.txt')
#now data is a 2D array of the same shape as the file -- three columns, about 100 rows

#len(data) gives you the length in the first dimension  -- in this case 100 rows
#first index specifies the row, as when specifying elements in a matrix
print(len(data))
#if we want to know the length in all dimensions, we can use shape
print(data.shape)

#Now we want to split the loaded data into three variables
# -- frequency, X and Y

# we could fill an array in a loop
# frequency = np.empty(data.shape[0])
# X = np.empty(data.shape[0])
# Y = np.empty(data.shape[0])
# for k in range(data.shape[0]):
#     frequency[k] = data[k, 0]
#     X[k] = data[k, 1]
#     Y[k] = data[k, 1]

#we can also take slices, here : means take everything along that dimension
#insteady of : we could use the same slicing syntax start:stop:step
# frequency = data[:, 0] #all rows, column index 0
# X = data[:, 1] #etc..
# Y = data[:, 2]

#or we can unpack along the first index
# but first we have to take the transpose (data.T) of the matrix data in order for the
# original column index to be first, i.e.
# frequency = data.T[0, :]
# X = data.T[1, :]
# Y = data.T[2, :]
#which can now be shortened to
frequency, X, Y = data.T

#and now we simply plot, frequency, X, and Y are simply numpy arrays
#plot everything together
fig, ax = plt.subplots()
ax.plot(frequency, X, '-o')
ax.plot(frequency, Y, '--s')


#plot in shared axes
fig2, axs2 = plt.subplots(2, 1, sharex=True, sharey=True)
axs2[0].plot(frequency, X)
axs2[1].plot(frequency, Y)

#plot Y against X
fig3, ax3 = plt.subplots()
ax3.plot(X, Y, '-o')
ax3.set_aspect('equal') #equal scaling on X and Y axis

plt.show()