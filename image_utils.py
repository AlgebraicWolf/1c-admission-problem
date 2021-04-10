import numpy as np

def deflate(image):
    '''Function that takes and image and returns array of points in the said image'''
    pixels = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if(image[i][j]):
                pixels.append((j, i))
                
    return np.array(pixels)
            

def centre_of_mass(pixels):
    '''Function that calculates centre of mass'''
    return np.sum(pixels, axis=0) / pixels.shape[0]


def distances(pixels, point):
    '''Calculate array of distances'''
    return np.linalg.norm(pixels-point, axis=1)

def get_side_vector(point, centre):
    '''Get vector that __should__ be close to the side'''
    vector = point - centre
    perpendicular = np.array([vector[1], -vector[0]])
    return perpendicular

def line_dist(point, start, vector):
    '''Get distance from point to the line'''
    return np.abs(vector[1]*point[0]-vector[0]*point[1] + vector[0]*start[1] - vector[1]*start[0]) / np.sqrt(np.sum(vector * vector))

def filter_points_out(pixels, start, vector, threshold):
    '''Leave only the points that are far enough from the approximated line'''
    left = []
    for point in pixels:
        if line_dist(point, start, vector) > threshold:
            left.append(point)
        
    return np.array(left)