from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from image_utils import *

filename = input("Specify input filename: ")
linewidth = int(input(
    "Would you mind providing us with an approximate line width for better performance? Enter it or zero (if you don't want us to know):"))

if linewidth == 0:
    linewidth = 20

print("Loading file...")
img = Image.open(filename)
# Get array of boolean pixels for more convenient solution
image = (np.array(img.getdata()).reshape(
    img.size[1], img.size[0], -1)[:, :, 0] != 255)

# Get array of black pixel coordinates from the array
pixels = deflate(image)

print("Loaded image of size {}x{}".format(img.size[1], img.size[0]))

centre = centre_of_mass(pixels)  # Get figure's centre of mass

d = distances(pixels, centre)

if np.max(d) - np.min(d) < linewidth:
    print("This seems to be a circle.")
    
    closest = pixels[np.argmin(d)]
    furthest = pixels[np.argmax(d)]

    inner = np.linalg.norm(closest - centre)
    outer = np.linalg.norm(furthest - centre)
    
    print("Its inner radius is {} and its outer radius is {}, giving approximate line width of {}.".format(inner, outer, outer - inner))
    exit(0)

print("Starting to deduce number of polygon's sides and their equations")

start_point = []  # Array of polygon sides' starting points
vectors = []  # Array of vectors parallel to the sides

while len(pixels) > 0:  # As long as there are pixels left
    d = distances(pixels, centre)  # Calculate distances to all the points
    closest = pixels[np.argmin(d)]  # Find the closest point. If we were to cast that touches the side, then it is approximate point of touch, and thus the side is perpendicular to the vector
    side_vector = get_side_vector(closest, centre)  # Find the vector parallel to the side
    pixels = filter_points_out(pixels, closest, side_vector, linewidth)  # Filter out the points that seem to be parts of the side
    start_point.append(closest)
    vectors.append(side_vector)

print("Found {} sides!".format(len(start_point)))

if len(start_point) == 3:
    print("This seems to be a triangle")
elif len(start_point) == 4:
    print("This seems to be a rectangle (I don't know what kind though).")
else:
    print("I have no idea what the hell is that! You might try refining threshold for better result.")
