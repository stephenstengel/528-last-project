#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Stephen Stengel  cs528  Final Project
#Simulation of gas particles with partial wall

#Simulation starts by putting all particles on the left side of a wall.

#The wall is removed midway through? At start?

import numpy
import matplotlib.pyplot as plt
import random

def main(args):
	print("Hi!")
	
	numpy.random.seed(3)
	
	xlow = -100
	xhigh = 100
	ylow = -100
	yhigh = 100
	# ~ xlow = -10
	# ~ xhigh = 10
	# ~ ylow = -10
	# ~ yhigh = 10
	# ~ xlow = -4
	# ~ xhigh = 4
	# ~ ylow = -4
	# ~ yhigh = 4
	
	xsize = abs( xhigh - xlow )
	ysize = abs( yhigh - ylow )
	
	# ~ numpoints = 10000
	numpoints = 100
	# ~ numpoints = 10
	
	numSteps = 100
	
	#Get xhigh up to wall
	wallstop = getxhighAbutment(xsize, xlow)
	
	print("wallstop: " + str(wallstop) + "\txlow: " + str(xlow) + "\txsize: " + str(xsize))
	
	#Create array to hold x and y positions of particles
	xpositions = numpy.random.randint(xlow, wallstop, numpoints)
	ypositions = numpy.random.randint(ylow, yhigh + 1, numpoints)
	
	# ~ hackx = []
	# ~ for i in range(numpoints):
		# ~ hackx.append(random.randint(xlow, wallstop))
	# ~ xpositions = numpy.array(hackx)
	
	xwallArray, ywallArray = createWallArray(xsize, ysize, xlow, xhigh, ylow, yhigh)
	
	print(xpositions)
	print(ypositions)
	
	simulate(numSteps, xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh)
	
	return 0


#Gets position of the left side of wall
def getxhighAbutment(xsize, xlow):
	wallxpos = xsize // 2
	#if xsize even, sub 1
	if xsize % 2 == 0:
		wallxpos -= 1
	
	return wallxpos + xlow

#Create array that holds the position of wall obstacles.
#Wall obstacles should always be at least 2x2 points!!!!!!!!!!!!!!!!
#Ones are walls, zeroes are spaces.
#There is a wall going down the middle with a hole in it in this version.
def createWallArray(xsize, ysize, xlow, xhigh, ylow, yhigh):
	# ~ empty = []
	# ~ xwallArray = numpy.array(empty)
	# ~ ywallArray = numpy.array(empty)
	xwallArray = []
	ywallArray = []
	
	wallxpos = getxhighAbutment(xsize, xlow)
	print("wallxpos: " + str(wallxpos))
	
	yFirstThird = (ysize // 3) + ylow
	ySecondThird = ((ysize * 2) // 3) + ylow
	
	for i in range(ylow, yhigh + 1):
		if i <= yFirstThird or i >= ySecondThird:
			# ~ print("ysize // 3 = " + str(ysize // 3) + "\ti: " + str(i) + "\ti < (ysize // 3): " + str(i < (ysize // 3)) + "\ti > ((2 * ysize) // 3): " + str(i > ((2 * ysize) // 3)))
			xwallArray.append(wallxpos)
			ywallArray.append(i)
			
			xwallArray.append(wallxpos + 1)
			ywallArray.append(i)
			
			

	# ~ return xwallArray, ywallArray
	return numpy.array(xwallArray), numpy.array(ywallArray)


#runs the simulation for some number of steps.
def simulate(numSteps, xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh):
	#print initial condition.
	
	
	for step in range(numSteps):
		printSimulation(xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, step)


def printSimulation(xArray, yArray, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, currentStep):
	plt.title("Simulation of gas with wall: time = " + str(currentStep))
	plt.xlabel("x")
	plt.ylabel("y")
	plt.scatter(xArray, yArray, color="Red")
	plt.scatter(xwallArray, ywallArray, color="Black")
	plt.xlim(xlow, xhigh)
	plt.ylim(ylow, yhigh)
	
	plt.show()
	
	# ~ fileName = "{}plot{:03}.png".format(plotsFolder, currentStep)
	# ~ plt.savefig(fileName)
	
	plt.clf()


if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
