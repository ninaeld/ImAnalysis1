import sys, os
import numpy as np
import matplotlib.pyplot as plt

def test_interp():
    # Tests the interp() function with a known input and output
    # Leads to error if test fails

    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([0.2, 0.4, 0.6, 0.4, 0.6, 0.8, 1.0, 1.1])
    x_new = np.array((0.5, 2.3, 3, 5.45))
    y_new_solution = np.array([0.2, 0.46, 0.6, 0.69])
    y_new_result = interp(y, x, x_new)
    np.testing.assert_almost_equal(y_new_solution, y_new_result)


def test_interp_1D():
    # Test the interp_1D() function with a known input and output
    # Leads to error if test fails

    y = np.array([0.2, 0.4, 0.6, 0.4, 0.6, 0.8, 1.0, 1.1])
    y_rescaled_solution = np.array([
        0.20000000000000001, 0.29333333333333333, 0.38666666666666671,
        0.47999999999999998, 0.57333333333333336, 0.53333333333333333,
        0.44000000000000006, 0.45333333333333331, 0.54666666666666663,
        0.64000000000000001, 0.73333333333333339, 0.82666666666666677,
        0.91999999999999993, 1.0066666666666666, 1.0533333333333335,
        1.1000000000000001
    ])
    y_rescaled_result = interp_1D(y, 2)
    np.testing.assert_almost_equal(y_rescaled_solution, y_rescaled_result)


def test_interp_2D():
    # Tests interp_2D() function with a known and unknown output
    # Leads to error if test fails

    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    matrix_scaled = np.array([[1., 1.4, 1.8, 2.2, 2.6, 3.],
                              [2., 2.4, 2.8, 3.2, 3.6, 4.],
                              [3., 3.4, 3.8, 4.2, 4.6, 5.],
                              [4., 4.4, 4.8, 5.2, 5.6, 6.]])

    result = interp_2D(matrix, 2)
    np.testing.assert_almost_equal(matrix_scaled, result)


def interp(y_vals, x_vals, x_new):
    # Computes interpolation at the given abscissas
    #
    # Inputs:
    #   x_vals: Given inputs abscissas, numpy array
    #   y_vals: Given input ordinates, numpy array
    #   x_new : New abscissas to find the respective interpolated ordinates, numpy
    #   arrays
    #
    # Outputs:
    #   y_new: Interpolated values, numpy array

    ################### PLEASE FILL IN THIS PART ###############################

    #array for y_new values the same size as x_new
    length = np.prod(x_new.shape)
    y_new = np.empty(length)
    #go through each x_new
    for i in range(length):
        #check if x_new is under the range
        if x_new[i] <= x_vals[0]:
            y_new[i] = y_vals[0]
        #check if x_new if over the range
        elif x_new[i] >= x_vals[x_vals.shape[0]-1]:
            y_new[i] = y_vals[y_vals.shape[0]-1]
        #if not calculate the y new value
        else:
            # look for the two values below and above x
            for j in range(1, x_vals.shape[0]):
                if x_new[i] <= x_vals[j]:
                    x0 = x_vals[j-1]
                    y0 = y_vals[j-1]
                    x1 = x_vals[j]
                    y1 = y_vals[j]
                    break
            y_new[i] = y0 * (1-((x_new[i]-x0)/(x1 - x0))) + y1 * ((x_new[i]-x0)/(x1-x0))

    return y_new


def interp_1D(signal, scale_factor):
    # Linearly interpolates one dimensional signal by a given scaling factor
    #
    # Inputs:
    #   signal: A one dimensional signal to be samples from, numpy array
    #   scale_factor: scaling factor, float
    #
    # Outputs:
    #   signal_interp: Interpolated 1D signal, numpy array

    ################### PLEASE FILL IN THIS PART ###############################
    #get the length of the signal
    length = np.prod(signal.shape)
    # create an x value array for the signal
    # start at 1 until length + 1
    x_values = np.arange(1, length+1)

    # create new x values with a array
    x_new = np.linspace(1, length, num=round(length*scale_factor))

    signal_interp = interp(signal, x_values, x_new)

    return signal_interp


def interp_2D(img, scale_factor):
    # Applies bilinear interpolation using 1D linear interpolation
    # It first interpolates in one dimension and passes to the next dimension
    #
    # Inputs:
    #   img: 2D signal/image (grayscale or RGB), numpy array
    #   scale_factor: Scaling factor, float
    #
    # Outputs:
    #   img_interp: interpolated image with the expected output shape, numpy array

    ################### PLEASE FILL IN THIS PART ###############################
    #get the length of the rescaled array
    length = round(img.shape[1]*scale_factor)
    #create an empty array of that length
    first_matrix = np.empty((0, length))

    #interpolate each row and append it to the new matrix
    for row in img:
        r = interp_1D(row, scale_factor)
        first_matrix = np.append(first_matrix, np.array([r]), axis=0)
    #transpose the matrix so it can be iterated over the rows
    transposed_matrix = first_matrix.transpose()
    #the length of the new matrix is calculated
    this_length = round(transposed_matrix.shape[1]*scale_factor)
    second_matrix = np.empty((0,this_length))
    #again interpolate each row and append it to the new matrix
    for row in transposed_matrix:
        r = interp_1D(row, scale_factor)
        second_matrix = np.append(second_matrix, np.array([r]), axis=0)
    #transpose the new matrix such that it gets its original orientation
    img_interp = second_matrix.transpose()
    return img_interp

def check_dimension(img, scale_factor):
    if ((len(img.shape)) == 2):
        #apply the interpolation for a grey image
        return interp_2D(img, scale_factor)
    elif ((len(img.shape)) == 3):
        #take apart each colour matrix and interpolate it separately
        red_values = interp_2D(img[:,:, 0], scale_factor)
        green_values = interp_2D(img[:,:,1], scale_factor)
        blue_values = interp_2D(img[:,:,2], scale_factor)
        #stack the colours and return the image
        return np.dstack((red_values, green_values, blue_values))

    else:
        print("Error: the image is of wrong dimension")
        return 0

# set arguments
#filename = 'bird.jpg'
filename = 'butterfly.jpg'
# filename = 'monkey_face.jpg'
scale_factor = 1.5  # Scaling factor

# Before trying to directly test the bilinear interpolation on an image, we
# test the intermediate functions to see if the functions that are coded run
# correctly and give the expected results.

print('...................................................')
print('Testing test_interp()...')
test_interp()
print('done.')

print('Testing interp_1D()....')
test_interp_1D()
print('done.')

print('Testing interp_2D()....')
test_interp_2D()
print('done.')

print('Testing bilinear interpolation of an image...')
# Read image as a matrix, get image shapes before and after interpolation
img = (plt.imread(filename)).astype('float')  # need to convert to float
in_shape = img.shape  # Input image shape

# Apply bilinear interpolation
img_int = check_dimension(img, scale_factor)
print('done.')

# Now, we save the interpolated image and show the results
print('Plotting and saving results...')
plt.figure()
plt.imshow(img_int.astype('uint8'))  # Get back to uint8 data type
filename, _ = os.path.splitext(filename)
plt.savefig('{}_rescaled.jpg'.format(filename))
plt.close()

plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(img.astype('uint8'), cmap="gray")
plt.title('Original')
plt.subplot(1, 2, 2)
plt.imshow(img_int.astype('uint8'), cmap="gray")
plt.title('Rescaled by {:2f}'.format(scale_factor))
print('Do not forget to close the plot window --- it happens:) ')
plt.show()

print('done.')
