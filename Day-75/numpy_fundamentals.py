"""
NumPy and Image Processing Practice

This project demonstrates the basics of NumPy arrays,
array dimensions, indexing, slicing, random numbers,
linear spacing, vector operations, matrix multiplication,
and basic image processing using NumPy and PIL.

Topics covered:
1. Creating 1D, 2D, and 3D NumPy arrays.
2. Checking shape and dimensions.
3. Indexing and slicing arrays.
4. Reversing arrays.
5. Generating random numbers.
6. Creating evenly spaced values.
7. Visualizing data using Matplotlib.
8. Performing vectorized arithmetic.
9. Broadcasting.
10. Matrix multiplication.
11. Reading images using PIL.
12. Converting images into NumPy arrays.
13. Inverting image colors using NumPy.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ============================ 1D NUMPY ARRAY ============================ #

my_array = np.array([1, 2, 3, 4])

print("1D NUMPY ARRAY")

print("Array:")
print(my_array)

print("\nShape:")
print(my_array.shape)

print("\nNumber of Dimensions:")
print(my_array.ndim)

print("\nFirst Element:")
print(my_array[0])


# ============================ 2D NUMPY ARRAY ============================ #

array_2d = np.array([
    [1, 2, 3, 9],
    [5, 6, 7, 8]
])


print("2D NUMPY ARRAY")

print("Array:")
print(array_2d)

print("\nShape:")
print(array_2d.shape)

print("\nNumber of Dimensions:")
print(array_2d.ndim)

print("\nElement at Row 2, Column 3:")
print(array_2d[1, 2])


# ============================ 3D NUMPY ARRAY ============================ #

mystery_array = np.array([
    [
        [0, 1, 2, 3],
        [4, 5, 6, 7]
    ],
    [
        [7, 86, 6, 98],
        [5, 1, 0, 4]
    ],
    [
        [5, 36, 32, 48],
        [97, 0, 27, 18]
    ]
])


print("3D NUMPY ARRAY")


print("Array:")
print(mystery_array)

print("\nNumber of Dimensions:")
print(mystery_array.ndim)

print("\nShape:")
print(mystery_array.shape)

print("\nElement at [2, 1, -1]:")
print(mystery_array[2, 1, -1])

print("\nComplete Row at [2, 1]:")
print(mystery_array[2, 1])

print("\nAll Values from the First Channel:")
print(mystery_array[:, :, 0])


# ============================ ARANGE ============================ #

"""
np.arange() creates evenly spaced integer values
within the specified range.
"""

a = np.arange(10, 30)

print("ARANGE")

print("Array from 10 to 29:")
print(a)

print("\nLast 3 Elements:")
print(a[-3:])


# ============================ REVERSE ARRAY ============================ #

reverse_array = np.flip(a)


print("REVERSED ARRAY")

print(reverse_array)


# ============================ RANDOM 3D ARRAY ============================ #

"""
Generate random integers between 0 and 99
inside a 3 x 3 x 3 array.
"""

rng = np.random.default_rng()

rint = rng.integers(
    0,
    100,
    size=(3, 3, 3)
)


print("RANDOM 3D ARRAY")

print(rint)


# ============================ LINSPACE ============================ #

"""
np.linspace() creates a specified number of
evenly spaced values between start and stop.
"""

x = np.linspace(
    start=0,
    stop=100,
    num=9
)

y = np.linspace(
    start=-3,
    stop=3,
    num=9
)


print("LINSPACE")

print("X values:")
print(x)

print("\nY values:")
print(y)


# ============================ LINE PLOT ============================ #

plt.figure(figsize=(10, 6))

plt.plot(x, y)

plt.title("Line Plot Using NumPy Linspace")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


# ============================ RANDOM IMAGE ============================ #

"""
Generate random RGB values for a 128 x 128 image.

The shape is:

128 -> Height
128 -> Width
3   -> RGB channels
"""

noise = np.random.rand(128, 128, 3)

print("RANDOM IMAGE DATA")

print("Array Shape:")
print(noise.shape)

print("\nRandom Image Array:")
print(noise)


# ============================ DISPLAY RANDOM IMAGE ============================ #

plt.figure(figsize=(6, 6))
plt.imshow(noise)
plt.axis("off")
plt.show()


# ============================ NUMPY VECTOR ADDITION ============================ #

v1 = np.array([4, 5, 2, 7])
v2 = np.array([2, 1, 3, 3])

list1 = [4, 5, 2, 7]
list2 = [2, 1, 3, 3]


print("NUMPY VECTOR ADDITION VS PYTHON LIST ADDITION")


addition = v1 + v2

print("NumPy Array Addition:")
print(addition)

py_lst_add = list1 + list2

print("\nPython List Addition:")
print(py_lst_add)


# ============================ VECTOR MULTIPLICATION ============================ #

multiplication = v1 * v2


print("NUMPY VECTOR MULTIPLICATION")


print(multiplication)


# ============================ NUMPY SCALAR OPERATIONS ============================ #


print("NUMPY SCALAR OPERATIONS")


array = np.array([1, 2, 3, 4])

print("Original Array:")
print(array)

print("\nArray + 1:")
print(array + 1)

print("\nArray * 2:")
print(array * 2)


# ============================ BROADCASTING ============================ #

two_d_array = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8]
])


print("NUMPY BROADCASTING")


print("Original 2D Array:")
print(two_d_array)

print("\nAdding 2:")
print(two_d_array + 2)


# ============================ MATRIX MULTIPLICATION ============================ #

a1 = np.array([
    [1, 3],
    [0, 1],
    [6, 2],
    [9, 7]
])

b1 = np.array([
    [4, 1, 3],
    [5, 8, 5]
])


print("MATRIX MULTIPLICATION")


print("Matrix A:")
print(a1)

print("\nMatrix B:")
print(b1)

print(
    f"\nMatrix A Shape: {a1.shape}"
)

print(
    f"Matrix A has {a1.shape[0]} rows "
    f"and {a1.shape[1]} columns."
)

print(
    f"\nMatrix B Shape: {b1.shape}"
)

print(
    f"Matrix B has {b1.shape[0]} rows "
    f"and {b1.shape[1]} columns."
)

print("\nDimensions of Result:")
print("(4 x 2) @ (2 x 3) = (4 x 3)")

print("\nUsing @ operator:")

matrix_result = a1 @ b1

print(matrix_result)

print("\nUsing np.matmul():")

c = np.matmul(a1, b1)

print(
    f"Result has {c.shape[0]} rows "
    f"and {c.shape[1]} columns."
)

print(c)


# ============================ LOAD IMAGE ============================ #

"""
Open an image using PIL and inspect its
type, dimensions, and color mode.
"""

img_pil = Image.open("yummy_macarons.jpg")


print("IMAGE INFORMATION")

print("Image Type:")
print(type(img_pil))

print("\nImage Size:")
print(img_pil.size)

print("\nImage Mode:")
print(img_pil.mode)

print("\nPIL Image Object:")
print(img_pil)

print("\nImage Shape:")
print(np.shape(img_pil))


# ============================ CONVERT IMAGE TO NUMPY ============================ #

"""
Convert the PIL image into a NumPy array.

Each pixel becomes a collection of
RGB values that NumPy can manipulate.
"""

img = np.array(img_pil)


print("IMAGE AS NUMPY ARRAY")


print("NumPy Image Shape:")
print(img.shape)

print("\nNumPy Image Data Type:")
print(img.dtype)


# ============================ DISPLAY ORIGINAL IMAGE ============================ #

plt.figure(figsize=(8, 6))
plt.imshow(img)
plt.axis("off")
plt.title("Original Image")
print("\nDisplaying Original Image...")
plt.show()


# ============================ INVERT IMAGE COLORS ============================ #

"""
Invert the image colors.

For an 8-bit RGB image:

New Pixel = 255 - Original Pixel
"""
inverted_img = 255 - img
plt.figure(figsize=(8, 6))
plt.imshow(inverted_img)
plt.axis("off")
plt.title("Inverted Image")
plt.show()

