import random
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from matplotlib import animation

N = 10
v = 0.1
refresh = 1/30
tol = 0.05
bounded = False
plus = False

class triPoint:
    def __init__(self, max_speed, bound=False):
        x = random.random()
        y = random.random()
        self.max_speed = max_speed
        self.point = np.array([x, y, 0])
        self.next = self.point
        self.__targets = []
        self.bound = bound

    def setTargets(self, target1, target2):
        self.__targets = [target1, target2]

    def targetPoint(self):
        a = self.__targets[0].point
        b = self.__targets[1].point
        c1 = a + 1/2 * (b-a) + np.sqrt(3)/2 * np.cross(b - a, [0,0,1])
        c2 = a + 1/2 * (b-a) - np.sqrt(3)/2 * np.cross(b - a, [0,0,1])
        cDist1 = np.linalg.norm(self.point - c1)
        cDist2 = np.linalg.norm(self.point - c2)
        if plus or cDist1 < cDist2:
            return c1
        else:
            return c2

    def nextPointCalc(self):
        d = self.targetPoint() - self.point
        dist = min(self.max_speed, np.linalg.norm(d))
        if np.linalg.norm(d) > tol:
            d = d / np.linalg.norm(d) * dist
        else:
            d = 0
        self.next = self.point + d
        if self.bound:
            self.next[0] = min(abs(self.next[0]), 1) * self.next[0]/abs(self.next[0])
            self.next[1] = min(abs(self.next[1]), 1) * self.next[0]/abs(self.next[1])


    def updatePoint(self):
        self.point = self.next

points = []

for i in range(N):
    points.append(triPoint(v, bound=bounded))

plots = []

plt.ion()
#fig = plt.figure()
ax = plt.gca(aspect='equal', adjustable='box')
ax.set_autoscale_on(True)

for i in range(N):
    choice1 = random.choice(points[:i] + points[i+1:])
    choice2 = random.choice(points[:i] + points[i+1:])
    while choice1 is choice2:
        choice2 = random.choice(points[:i] + points[i+1:])
    points[i].setTargets(choice1, choice2)
    plots.append(plt.plot([points[i].point[0]], [points[i].point[1]],'ro'))

while plt.fignum_exists(1):
    for point in points:
        point.nextPointCalc()
    for i in range(len(points)):
        points[i].updatePoint()
        plots[i][0].set_xdata(points[i].point[0])
        plots[i][0].set_ydata(points[i].point[1])
    ax.relim()
    ax.autoscale_view(True,True,True)
    if bounded:
        ax.set_xbound(-2,2)
        ax.set_ybound(-2,2)
    else:
        ylim = ax.get_ylim()
        xlim = ax.get_xlim()
        ax.set_xbound((min(xlim[0],ylim[0])-1,max(xlim[1],ylim[1])+1))
        ax.set_ybound((min(xlim[0],ylim[0])-1,max(xlim[1],ylim[1])+1))
    plt.pause(refresh)
    distances = []
    for point in points:
        distances.append(np.linalg.norm(point.point - point.targetPoint()))
    if max(distances) < tol:
        break

while plt.fignum_exists(1):
    plt.pause(refresh)
