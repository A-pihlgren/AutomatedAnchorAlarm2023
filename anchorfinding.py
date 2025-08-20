import numpy as np
import matplotlib.pyplot as plt
import sys
from decimal import Decimal

midpoint_x = 0
midpoint_y = 0

#Finds intersection points of two lines. It takes three points as arguments/positions of the boat and returns the point of intersection of three
def find_intersection(p1, p2, p3):
    #checking if any position is identical, this can result in division by zero errors
    if (p1 == p2 or p1 == p3 or p2 == p3):
        return None
    
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    if x2 - x1 == 0:
        m1 = float('inf')
    else:
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
    
    if x3 - x2 == 0:
        m2 = float('inf')
    else:
        m2 = (p3[1] - p2[1]) / (p3[0] - p2[0])
    
    #Check if the lines are parallel
    if m1 == m2:
        return None
    
    if m1 == 0.0:
        mp1 = 0
    else:
        mp1 = -1 / m1
    if m2 == 0.0:
        mp2 = 0
    else:
        mp2 = -1 / m2
    
    midpoint1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    midpoint2 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
    
    b1 = midpoint1[1] - mp1 * midpoint1[0]
    b2 = midpoint2[1] - mp2 * midpoint2[0]
    #This was added because of division by zero error
    try:
        x = (b2 - b1) / (mp1 - mp2)
        y = mp1 * x + b1
    except:
        return None
    
    #print(x, y)
    
    return (round(x, 5), round(y, 5))

#This function calculates the likelihood of a location being the actual anchor location
def liklidistribution(x, y, midpoint_x, midpoint_y, radius):
    distance = np.sqrt((x - midpoint_x)**2 + (y - midpoint_y)**2)
    return 1 / (2 * np.pi * radius) * np.exp(-distance / radius)

#updates the probability of each location being the center point using bayes
def calcProbability(prior_prob, checkifincircle_vals):
    return prior_prob * checkifincircle_vals / np.sum(prior_prob * checkifincircle_vals)

#Takes two arguments, the prior probability and the list of boat positions. It calculates a midpoint and radius using the given locations to find intersections. If it receives an intersection point it checks that the point is not to far away and adds it to the list outputting
#The likelihood of each point is calculated, the prior probability of each point is updated using calcprobability.
def updateProbability(prior_prob, positionsLatLong):
    radius = 0
    for x, y in positionsLatLong:
        radius += np.sqrt((x - midpoint_x)**2 + (y - midpoint_y)**2)
    radius /= len(positionsLatLong)

    intersection_points = []

    p1 = positionsLatLong[0]
    p2 = positionsLatLong[1]
    for i in range(2, len(positionsLatLong)):
        print(i)
    
        p3 = positionsLatLong[i]
        intersection_point1 = find_intersection(p1, p2, p3)
    
        if intersection_point1:
            h, k = intersection_point1
        
            if (not(h > (p1[0] + 1) or h < (p1[0] - 1)) or not(k > (p1[1] + 1) or k < (p1[1] - 1))):
                intersection_points.append(intersection_point1)
    
        p1 = p2
        p2 = p3

    for x, y in intersection_points:
        checkifincircle_vals = liklidistribution(x, y, X, Y, radius)
        prior_prob = calcProbability(prior_prob, checkifincircle_vals)
    print(intersection_points)
    return prior_prob

#Test 6
#positionsLatLong = [(-15.426, 28.13001), (-15.42509, 28.13078), (-15.42509, 28.13076), (-15.42507, 28.13076), (-15.42509, 28.13077)
positionsLatLong = [(-15.42599, 28.13078), (-15.42599, 28.13076), (-15.42597, 28.13076), (-15.42599, 28.13077), (-15.42598, 28.13077)]

#Test 7
#positionsLatLong = [(-15.42371, 28.13051), (-15.42372, 28.13046), (-15.42372, 28.13049), (-15.42372, 28.13045), (-15.42372, 28.13051)]
#positionsLatLong = [(28.13164,-15.42631), (28.13166,-15.42641), (28.13169,-15.42621), (28.13172,-15.42651), (28.13190,-15.42659)]
#positionsLatLong = [(28.13093, -15.42542), (28.13089, -15.42553), (28.13094, -15.42547), (28.13091, -15.42548), (28.13089, -15.42551)]
#positionsLatLong = [(28.13164, -15.42631), (28.13168, -15.42625), (28.13166, -15.42628), (28.13161, -15.42630), (28.13163, -15.42634)]

# Define the prior probability distribution
x1, y1 = positionsLatLong[0]
X, Y = np.meshgrid(np.linspace(x1 - 0.001, x1 + 0.001, 100), np.linspace(y1 - 0.001, y1 + 0.001, 50))

prior_prob = np.ones(X.shape) / (100 * 100)

prior_prob /= np.sum(prior_prob)
# Define the circle parameters

# Update the posterior after each observation
prior_prob = updateProbability(prior_prob, positionsLatLong)

# Find the most likely midpoint
arg_max = np.argmax(prior_prob)
midpoint_x, midpoint_y = np.unravel_index(arg_max, X.shape)

# Convert the indices to actual values
midpoint_x1 = X[midpoint_x, midpoint_y]

midpoint_y1 = Y[midpoint_x, midpoint_y]

plt.imshow(prior_prob, origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()])
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()
print("Estimated midpoint: ({:.5f}, {:.5f})".format(midpoint_x1, midpoint_y1))
