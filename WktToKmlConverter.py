#Author: Jose Antonio Ciccio C.

#Script intended to handle and convert wkt multipolygons into kml multipolygons

#File input format:
#Poloygon name -8-AL-PB94457|0100007|010000600303|NAME|P|1.13.4|2|MULTIPOLYGON (((-86.716765469999984 34.670241110000063, ...)
#Expecting to have a name at field 4 and to process a multypolygon

#!/usr/bin/env python

import sys
import re
import simplekml
import argparse
import random
import os
import pdb
import copy

def createKMLPolygon(lines):
	kml = simplekml.Kml()
	for idx,l in enumerate(lines):
		splitted = re.findall(r"[^ ,]+", l)
		spl = [float(i) for i in splitted]
		coords = zip(splitted[::2],splitted[1::2])
		pol = kml.newpolygon(name='Polygon '+str(idx) )
		pol.outerboundaryis = coords		
		pol.style.polystyle.color = simplekml.Color.red

	return kml

def splitArrayByPolygons(array):
	splittedArray = []
	for item in array:
		splittedArray.append(splitByPolygons(item))
	return splittedArray

def splitByPolygons(wkt):
	return re.findall(r"\(?\(\(([^)]*)", wkt)

def readFile(filename):
	array = []
	with open(filename, "r") as ins:
	    for line in ins:
	        array.append(line)
    
def createDirectory (name):
	if not os.path.exists(name):
		os.makedirs(name)

def writeFile(filename, data):
	fo = open(filename, "wb")
	fo.write(data);

def main():
	#	Argument Parser
	print "Going to split wkt into files to be processed"
	parser = argparse.ArgumentParser(description='Converter of WKT\'s linestrings to KML')
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),default=sys.stdin)
	args = parser.parse_args()
	content = args.infile.read().splitlines()
	lineNumber = 1
	extension = ".wkt"
	kmlExtension = ".kml"
	wktDirectory = "wkt_splitted/"
	kmlDirectory = "kml_splitted/"
	kmlDirectoryGrouped = "kml_grouped/"
	content_data = {}

	#directory creation for outputs
	createDirectory(wktDirectory)
	createDirectory(kmlDirectory)
	createDirectory(kmlDirectoryGrouped)

	#processing and generating a single file per each entry
	for item in content:
		
		parts = item.split("|")
		print "Processing line %s with name %s" % (lineNumber , parts[3])
		filename = parts[3].replace(" ", "_").lower()

		for part in parts:
			#print "%s \n" %part
			if "MULTIPOLYGON" in part:
				file = "%s%d%s" %(filename, lineNumber, extension)
				kmlFile = "%s%d%s" %(filename, lineNumber, kmlExtension)
				if not filename in content_data:
					content_data[filename] = []
				
				content_data[filename].append(part)
				print "Creating wkt file called: %s" % (file)
				writeFile(wktDirectory + file, part)
				print "Creating kml file called: %s" % (kmlFile)
				cleanInput = splitByPolygons(part)
				kmlUnit = createKMLPolygon(cleanInput)
				writeFile(kmlDirectory + kmlFile, kmlUnit.kml())
		lineNumber = lineNumber + 1

	#grouping files per location name
	for key, group in content_data.iteritems():
		group = list(set(group))
		print "Processing group %s" % key
		kmlGroupFile = "%s%s" %(key, kmlExtension)
		print "Creating kml file called: %s" % (kmlGroupFile)
		cleanInput = splitArrayByPolygons(group)
		#we can proceed and create a kml with the consolidated school data
		flattenList = sum(cleanInput,[]) #converts array of arrays into a single array
		kmlUnit = createKMLPolygon(flattenList)
		writeFile(kmlDirectoryGrouped + kmlGroupFile, kmlUnit.kml())

if __name__ == "__main__":
	main()
