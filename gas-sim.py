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
import math
import os


def main(args):
	print("Hi!")
	
	print("Clearing old plots...")
	plotsFolder = "../frames/"
	videoFolder = "../video/"
	
	os.system("rm " + plotsFolder + "*.png")
	print("Done!")
	
	numpy.random.seed(3)
	
	# ~ xlow = -10000
	# ~ xhigh = 10000
	# ~ ylow = -10000
	# ~ yhigh = 10000
	# ~ xlow = -1000
	# ~ xhigh = 1000
	# ~ ylow = -1000
	# ~ yhigh = 1000
	xlow = -100
	xhigh = 100
	ylow = -100
	yhigh = 100
	# ~ xlow = -50
	# ~ xhigh = 50
	# ~ ylow = -100
	# ~ yhigh = 100
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
	numpoints = 1000
	# ~ numpoints = 100
	# ~ numpoints = 10
	
	# ~ numSteps = 100000
	# ~ numSteps = 50000
	numSteps = 30000
	numFrames = 30
	stepSizeGraphing = numSteps // numFrames + 1
	
	
	#Get xhigh up to wall
	wallstop = getxhighAbutment(xsize, xlow)
	
	# ~ print("wallstop: " + str(wallstop) + "\txlow: " + str(xlow) + "\txsize: " + str(xsize))
	
	#Create array to hold x and y positions of particles
	xpositions = numpy.random.randint(xlow, wallstop, numpoints)
	ypositions = numpy.random.randint(ylow, yhigh + 1, numpoints)
	
	# ~ hackx = []
	# ~ for i in range(numpoints):
		# ~ hackx.append(random.randint(xlow, wallstop))
	# ~ xpositions = numpy.array(hackx)
	
	xwallArray, ywallArray = createWallArray(xsize, ysize, xlow, xhigh, ylow, yhigh)
	
	# ~ print(xpositions)
	# ~ print(ypositions)
	
	simulate(numSteps, xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, ysize, stepSizeGraphing, plotsFolder)
	
	
	createAnimations(plotsFolder, videoFolder)
	
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
	# ~ print("wallxpos: " + str(wallxpos))
	
	# ~ yFirstThird = (ysize // 3) + ylow
	# ~ ySecondThird = ((ysize * 2) // 3) + ylow
	
	yFirstThird, ySecondThird = yPartitions(ysize, ylow)
	
	for i in range(ylow, yhigh + 1):
		if i <= yFirstThird or i >= ySecondThird:
			# ~ print("ysize // 3 = " + str(ysize // 3) + "\ti: " + str(i) + "\ti < (ysize // 3): " + str(i < (ysize // 3)) + "\ti > ((2 * ysize) // 3): " + str(i > ((2 * ysize) // 3)))
			xwallArray.append(wallxpos)
			ywallArray.append(i)
			
			xwallArray.append(wallxpos + 1)
			ywallArray.append(i)
			
			

	# ~ return xwallArray, ywallArray
	return numpy.array(xwallArray), numpy.array(ywallArray)


#Returns the y partition points for the wall.
def yPartitions(ysize, ylow):
	# ~ yFirstThird = (ysize // 3) + ylow
	# ~ ySecondThird = ((ysize * 2) // 3) + ylow
	
	yFirstThird = ((4 * ysize) // 10) + ylow
	ySecondThird = ((ysize * 6) // 10) + ylow
	
	return yFirstThird, ySecondThird

#runs the simulation for some number of steps.
def simulate(numSteps, xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, ysize, stepSizeGraph, plotsFolder):
	#print initial condition
	printSimulation(xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, 0, plotsFolder)
	
	movesArray = numpy.random.randint(1, 5, size=(numSteps, len(xpositions)))
	
	NORTH = 1
	EAST = 2
	SOUTH = 3
	WEST = 4
	
	for step in range(1, numSteps):
		# ~ print(movesArray[step])
		#random walk the arrays.
		# ~ print("xpos b4 west")
		# ~ print(xpositions)
		xpositions -= numpy.where(movesArray[step] == WEST, 1, 0)
		# ~ print("xpos after west")
		# ~ print(xpositions)
		
		xpositions += numpy.where(movesArray[step] == EAST, 1, 0)
		ypositions += numpy.where(movesArray[step] == NORTH, 1, 0)
		ypositions -= numpy.where(movesArray[step] == SOUTH, 1, 0)
		
		#fix error points.
		xpositions, ypositions = fixInWall(xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, ysize)
		
		#print updated field
		if step % stepSizeGraph == 0:
			printSimulation(xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, step, plotsFolder)


#Moves points to a good position if they impact walls.
def fixInWall(xpositions, ypositions, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, ysize):
	#Fix out of bounds
	for i in range(len(xpositions)):
		if xpositions[i] < xlow:
			xpositions[i] = xlow
		elif xpositions[i] > xhigh:
			xpositions[i] = xhigh
		
		if ypositions[i] < ylow:
			ypositions[i] = ylow
		elif ypositions[i] > yhigh:
			ypositions[i] = yhigh
	
	#fix wall collision
	#get wall coords
	leftSideWall = math.inf
	rightSideWall = -math.inf
	
	yFirstThird, ySecondThird = yPartitions(ysize, ylow) #move up functions and pass?
	
	
	for i in range(len(xwallArray)):#move up functions loops
		if xwallArray[i] < leftSideWall:
			leftSideWall = xwallArray[i]
		if xwallArray[i] > rightSideWall:
			rightSideWall = xwallArray[i]
	
	#for each xy coord,
	for i in range(len(xpositions)):
		# ~ #If at a wall place
		# ~ #left
		if xpositions[i] == leftSideWall:
			#if not in free middle third y section.
			if ypositions[i] <= yFirstThird or ypositions[i] >= ySecondThird:
				xpositions[i] -= 1
		
		#right
		elif xpositions[i] == rightSideWall:
			if ypositions[i] <= yFirstThird or ypositions[i] >= ySecondThird:
				xpositions[i] += 1
		
	
	return xpositions, ypositions


def printSimulation(xArray, yArray, xwallArray, ywallArray, xlow, xhigh, ylow, yhigh, currentStep, plotsFolder):
	plt.title("Simulation of gas with wall: time = " + str(currentStep))
	plt.xlabel("x")
	plt.ylabel("y")
	plt.scatter(xArray, yArray, color="Red")
	plt.scatter(xwallArray, ywallArray, color="Black")
	plt.xlim(xlow, xhigh)
	plt.ylim(ylow, yhigh)
	
	# ~ plt.show()
	
	fileName = "{}plot{:05}.png".format(plotsFolder, currentStep)
	plt.savefig(fileName)
	
	plt.clf()


#Creates the animation from the saved files.
def createAnimations(plotsFolder, outputFolder):
	#This compresses the .pngs
	#os.system("optipng " + plotsFolder + "*.png")
	
	delay = 5
	
	print("Combining into an .mkv...")
	os.system("convert -delay " + str(delay) + " " + plotsFolder + "*.png " + outputFolder + "output.mkv")
	
	print("Combining into an .mp4...")
	os.system("convert -delay " + str(delay) + " " + plotsFolder + "*.png " + outputFolder + "output.mp4")
	
	print("Combining into a .gif...")
	os.system("convert -delay " + str(delay) + " " + plotsFolder + "*.png " + outputFolder + "output.gif")


if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
