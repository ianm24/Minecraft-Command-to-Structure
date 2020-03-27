# Copyright 2020 Ian McDowell
nbtPath = '../lib/NBT'
import sys
sys.path.append(nbtPath+'/nbt')
import nbt
from nbt import *

# Validates structure size
def checkStructSize(structSize):
	for x in range(0,3):
		if int(structSize[x]) > 32 or int(structSize[x]) < 1:
			return False
	return True

# Validates structure name
def checkstructName(structName):
	allowedChars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','_','-']
	for x in range(0,len(structName)):
		if structName.lower()[x] not in allowedChars:
			return False
	return True

# Validates block type values
def checkBlockType(blockType):
	allowedTypes = ["repeating","chain","impulse"]
	return blockType.lower() in allowedTypes

# Validates block direction values
def checkBlockDirection(blockDirection):
	allowedDirectionsString = ["up","down","north","south","east","west"]
	return blockDirection.lower() in allowedDirectionsString

# Checks if the line direction will stay inside the structure
def checkLineDirection(lineDirection,lineStartCoordinates,structSize):
	if lineDirection == "west" and int(lineStartCoordinates[0]) - 1 <= 0:
		return False
	elif lineDirection == "down" and int(lineStartCoordinates[1]) - 1 <= 0:
		return False
	elif lineDirection == "north" and int(lineStartCoordinates[2]) - 1 <= 0:
		return False
	else:
		return True

# Validates conditional status values
def checkConditionalStatus(conditionalStatus):
	return conditionalStatus.lower() == "false" or conditionalStatus.lower() == "true"

# Validates coordinate values
def checkCoordinates(coordinates):
	for x in range(0,3):
		if int(coordinates[x]) > 31 or int(coordinates[x]) < 0:
			return False
	return True

# Makes sure there isn't another block in the same coordinate
def checkCoordEmpty(coordinates, usedCoordList):
	return not coordinates in usedCoordList

# Converts from direction String format to direction list format
def getDirectionValue(direction):
	if direction == "east":
		return [0,1]
	elif direction == "west":
		return [0,-1]
	elif direction == "up":
		return [1,1]
	elif direction == "down":
		return [1,-1]
	elif direction == "south":
		return [2,1]
	elif direction == "north":
		return [2,-1]
	else:
		return False

# Converts from direction list format to direction String format
def getDirectionName(direction):
	if direction == [0,1]:
		return "east"
	elif direction == [0,-1]:
		return "west"
	elif direction == [1,1]:
		return "up"
	elif direction == [1,-1]:
		return "down"
	elif direction == [2,1]:
		return "south"
	elif direction == [2,-1]:
		return "north"
	else:
		return False

# Returns the structure's size given which coordinates have blocks
def getStructureSize(usedCoordList):
	maxX = 1
	maxY = 1
	maxZ = 1
	for coordinate in usedCoordList:
		if coordinate[0] >= maxX:
			maxX = coordinate[0] + 1
		if coordinate[1] >= maxY:
			maxY = coordinate[1] + 1
		if coordinate[2] >= maxZ:
			maxZ = coordinate[2] + 1
	return [maxX,maxY,maxZ]


# Given block data, validates input and returns data as list
def makeBlock(blockType,blockDirection,conditional,blockCoordinates,command,lineNumber,usedCoordList):
	if not checkBlockType(blockType):
		print("BlockTypeError on Line " + str(lineNumber) + ": \"" + str(blockType) +
			"\" is not a valid block type. Block types must be either \"repeating\",\"chain\", or \"impulse\".")
		exit()
	allowedDirectionsList = [[0,1],[0,-1],[1,1],[1,-1],[2,1],[2,-1]]
	if blockDirection in allowedDirectionsList:
		blockDirection = getDirectionName(blockDirection)
	if not checkBlockDirection(blockDirection):
		print("InvalidDirectionError on Line " + str(lineNumber) + ": \"" + str(blockDirection) +
			"\" is not a valid direction. Directions must be either \"up\",\"down\",\"north\",\"south\",\"east\", or \"west\".")
		exit()
	if not checkConditionalStatus(conditional):
		print("BlockConditionalStatusError on Line " + str(lineNumber) + ": \"" + str(conditional) +
			"\" is not a valid block conditional status. Block conditional status\' must be True or False.")
		exit()
	if not checkCoordinates(blockCoordinates):
		print("BlockCoordinateOutOfRangeError on Line " + str(lineNumber) + ": \"" + str(blockCoordinates) +
			"\" is an invalid block coordinate. Block coordinate values must be less than the structure size and greater than or equal to zero.")
		exit()
	if not checkCoordEmpty(blockCoordinates,usedCoordList):
		print("BlockCoordinateUsedError on Line " + str(lineNumber) + ": \"" + str(blockCoordinates) +
			"\" has already been occupied. Please make sure to only put one block at a certain coordinate.")
		exit()
	return [blockType,blockDirection,conditional,blockCoordinates,command]


# Uses file data from parseFile() to create the structure's NBT file
def makeNBTFile(fileData):
	STRUCT_INFO = fileData[0]
	BLOCK_LIST = fileData[1]
	USED_COORDS_LIST = fileData[2]
	AIR_BLOCKS = []

	print("Writing " + STRUCT_INFO[1] + ".nbt")
	print([STRUCT_INFO,BLOCK_LIST])
	print(STRUCT_INFO[1] + ".nbt Successfully Written")

# Parses the MCS file and returns all relavent file data
def parseFile(fileName):
	print("Parsing " + fileName)
	mcsFile = open(fileName, 'r')
	line = mcsFile.readline()
	lineNumber = 1

	LINE_MODE = False
	CURR_LINE_LENGTH = 0
	CURR_LINE_DIRECTION = [-1,-1]
	STRUCT_INFO = [[-1,-1,-1],""]
	BLOCK_LIST = []
	USED_COORDS_LIST = []
	LINE_START_COORDINATES = []
	while line:
		# empty line or a comment
		if line[0] == '\n' or line[0] == '#':
			line = mcsFile.readline()
			lineNumber += 1
			continue
		lineText = line.split()
		# Creating Lines
		if LINE_MODE:
			if lineText[0] ==  '}':
				LINE_MODE = False
				LINE_START_COORDINATES = []
				CURR_LINE_LENGTH = 0
				line = mcsFile.readline()
				lineNumber += 1
				continue
			if nextLineBlock[CURR_LINE_DIRECTION[0]] >= 32 or nextLineBlock[CURR_LINE_DIRECTION[0]] < 0:
				print("LineOutOfBoundsError on Line " + str(lineNumber) + ": \"" + str(nextLineBlock) +
						"\" is outside of the structure. Make sure your line fits inside of the structure.")
				exit()
			blockType = lineText[0]
			conditional = lineText[1]
			command = ""
			for x in range(2,len(lineText)):
				command += lineText[x] + " "
			lineBlockData = makeBlock(blockType,CURR_LINE_DIRECTION,conditional,nextLineBlock[:],command,lineNumber,USED_COORDS_LIST)
			USED_COORDS_LIST.append(nextLineBlock[:])
			BLOCK_LIST.append(lineBlockData[:])
			CURR_LINE_LENGTH += 1
			nextLineBlock[CURR_LINE_DIRECTION[0]] += CURR_LINE_DIRECTION[1]


		# Initialization variables
		elif lineText[0] == "init":
			if lineText[1] == "structName":
				STRUCT_INFO[1] = str(lineText[2])
				if not checkstructName(STRUCT_INFO[1]):
					print("StructureNameError on Line " + str(lineNumber) + ": \"" + str(STRUCT_INFO[1]) +
						"\" contains invalid characters. Structure names should only contain letters [A-Z], numbers [0-9], underscores \'_\', and hyphens \'-\'.")
					exit()
			else:
				print("InitializationError on Line " + str(lineNumber) + ": \"" + str(lineText[1]) +
					"\" is not an initialization command. Acceptable commands are: \"structName\".")
				exit()


		# New Objects
		elif lineText[0] == "new":
			if STRUCT_INFO[1] == "":
				print("InitializationError on Line " + str(lineNumber) + ": \"" + str(lineText[0]) +
					"\" called before structure initialization. Structure name must be initialized before creating objects.")
				exit()
			# New Blocks
			if lineText[1] == "block":
				blockType = lineText[2]
				blockDirection = lineText[3]
				conditional = lineText[4]
				blockCoordinates = [int(lineText[5]),int(lineText[6]),int(lineText[7])]
				command = ""
				for x in range(8,len(lineText)):
					command += lineText[x] + " "
				blockData = makeBlock(blockType,blockDirection,conditional,blockCoordinates,command,lineNumber,USED_COORDS_LIST)
				USED_COORDS_LIST.append(blockCoordinates)
				BLOCK_LIST.append(blockData[:])
			# New Lines
			elif lineText[1] == "line":				
				lineStartCoordinates = [int(lineText[2]),int(lineText[3]),int(lineText[4])]
				if not checkCoordinates(lineStartCoordinates):
					print("LineCoordinateOutOfRangeError on Line " + str(lineNumber) + ": \"" + str(lineStartCoordinates) +
						"\" is an invalid line start coordinate. Line start coordinate values must be inside the structure.")
					exit()
				lineDirection = lineText[5]
				if not checkBlockDirection(lineDirection):
					print("InvalidDirectionError on Line " + str(lineNumber) + ": \"" + str(lineDirection) +
						"\" is not a valid direction. Directions must be either \"up\",\"down\",\"north\",\"south\",\"east\", or \"west\".")
					exit()
				if not checkLineDirection(lineDirection,lineStartCoordinates,STRUCT_INFO[0]):
					print("LineDirectionError on Line " + str(lineNumber) + ": \"" + str(lineDirection) +
						"\" points the line outside of the structure. Remember \"east\" points in the positive X direction," +
						"\"west\" points in the negative X direction, \"up\" points in the positive Y direction,\"down\" points in the negative Y direction," +
						" \"south\" points in the positive Z direction, and \"north\" points in the negative Z direction.") 
					exit()
				LINE_MODE = True
				CURR_LINE_DIRECTION = getDirectionValue(lineDirection)
				LINE_START_COORDINATES = lineStartCoordinates
				nextLineBlock = [lineStartCoordinates[0],lineStartCoordinates[1],lineStartCoordinates[2]]
			else:
				print("NewObjectError on Line " + str(lineNumber) + ": \"" + str(lineText[1]) +
					"\" is not an object command. Acceptable commands are: \"block\", and \"line\".")
				exit()
		else:
			print("UnknownCommandError on Line " + str(lineNumber) + ": \"" + str(lineText[0]) +
					"\" is not a valid command. Acceptable commands outside of a line are: \"init\", and \"new\".")
			exit()
		line = mcsFile.readline()
		lineNumber += 1

	STRUCT_INFO[0] = getStructureSize(USED_COORDS_LIST)
	mcsFile.close()
	print(fileName + " Successfully Parsed")
	fileData = [STRUCT_INFO,BLOCK_LIST,USED_COORDS_LIST]
	return fileData


def main():
	fileName = str(input("Enter the name of the MCS file: "))
	if ".mcs" not in fileName[len(fileName)-4:]:
		print("InvalidFileNameError: \"" + str(fileName) + "\" was not an MCS file.")
		exit()
	makeNBTFile(parseFile(fileName))

if __name__ == "__main__":
	main()
