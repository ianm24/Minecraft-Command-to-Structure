nbtPath = '../lib/NBT'
import sys
sys.path.append(nbtPath+'/nbt')
import nbt
from nbt import *

def makeNBTFile(fileData):
	STRUCT_SIZE = fileData[0]
	STRUCT_NAME = fileData[1]
	BLOCK_LIST = fileData[2]
	LINE_LIST = fileData[3]
	print(fileData)

def checkStructSize(size):
	return int(size) >= 1 and int(size) <= 32

def checkstructName(structName):
	allowedChars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','_','-']
	for x in range(0,len(structName)):
		if structName.lower()[x] not in allowedChars:
			return False
	return True

def checkBlockType(blockType):
	allowedTypes = ["repeating","chain","impulse"]
	return blockType.lower() in allowedTypes

def checkBlockDirection(blockDirection):
	allowedDirections = ["up","down","north","south","east","west"]
	return blockDirection.lower() in allowedDirections

def checkConditionalStatus(conditionalStatus):
	return conditionalStatus.lower() == "false" or conditionalStatus.lower() == "true"

def checkCoordinate(coordinate):
	return int(coordinate) >= 0 and int(coordinate) <= 31

def checkCoordinateFit(coordinates,structSize):
	for x in range(0,2):
		if int(coordinates[x]) > (int(structSize[x]) - 1):
			return False
	return True


def parseFile(fileName):
	mcsFile = open(fileName, 'r')
	line = mcsFile.readline()
	lineNumber = 1

	LINE_MODE = False
	STRUCT_SIZE = [-1,-1,-1]
	STRUCT_NAME = ""
	BLOCK_LIST = []
	LINE_LIST = []
	while line:
		if line[0] == "\n" or line[0] == "#":
			# empty line or a comment
			line = mcsFile.readline()
			lineNumber += 1
			continue
		lineText = line.split()
		if lineText[0] == "init":
			if lineText[1] == "xSize":
				STRUCT_SIZE[0] = int(lineText[2])
				if not checkStructSize(STRUCT_SIZE[0]):
					print("StructureSizeError on Line " + str(lineNumber) + ": \"" + str(STRUCT_SIZE[0]) + "\" is an invalid structure size value. Structure size values must be integers in the range [1-32].")
					exit()
			elif lineText[1] == "ySize":
				STRUCT_SIZE[1] = int(lineText[2])
				if not checkStructSize(STRUCT_SIZE[1]):
					print("StructureSizeError on Line " + str(lineNumber) + ": \"" + str(STRUCT_SIZE[1]) + "\" is an invalid structure size value. Structure size values must be integers in the range [1-32].")
					exit()
			elif lineText[1] == "zSize":
				STRUCT_SIZE[2] = int(lineText[2])
				if not checkStructSize(STRUCT_SIZE[2]):
					print("StructureSizeError on Line " + str(lineNumber) + ": \"" + str(STRUCT_SIZE[2]) + "\" is an invalid structure size value. Structure size values must be integers in the range [1-32].")
					exit()
			elif lineText[1] == "structName":
				STRUCT_NAME = str(lineText[2])
				if not checkstructName(STRUCT_NAME):
					print("StructureNameError on Line " + str(lineNumber) + ": \"" + str(STRUCT_NAME) + "\" contains invalid characters. Structure names should only contain letters [A-Z], numbers [0-9], underscores \'_\', and hyphens \'-\'.")
					exit()
			else:
				print("InitializationError on Line " + str(lineNumber) + ": \"" + str(lineText[1]) + "\" is not an initializaiton command. Acceptable commands are: \"xSize\",\"ySize\",\"zSize\", and \"structName\".")
				exit()
		elif lineText[0] == "new":
			#new code
			if lineText[1] == "block":
				blockType = lineText[2]
				if not checkBlockType(blockType):
					print("BlockTypeError on Line " + str(lineNumber) + ": \"" + str(blockType) + "\" is not a valid block type. Block types must be either \"repeating\",\"chain\", or \"impulse\".")
					exit()
				blockDirection = lineText[3]
				if not checkBlockDirection(blockDirection):
					print("BlockDirectionError on Line " + str(lineNumber) + ": \"" + str(blockDirection) + "\" is not a valid block direction. Block directions must be either \"up\",\"down\",\"north\",\"south\",\"east\", or \"west\".")
					exit()
				conditional = lineText[4]
				if not checkConditionalStatus(conditional):
					print("BlockConditionalStatusError on Line " + str(lineNumber) + ": \"" + str(conditional) + "\" is not a valid block conditional status. Block conditional status\' must be True or False.")
					exit()
				blockCoordinates = [lineText[5],lineText[6],lineText[7]]
				if not checkCoordinate(blockCoordinates[0]):
					print("BlockCoordinateError on Line " + str(lineNumber) + ": \"" + str(blockCoordinates[0]) + "\" is an invalid coordinate value. Block coordinate values must be integers in the range [0-31].")
					exit()
				if not checkCoordinate(blockCoordinates[1]):
					print("BlockCoordinateError on Line " + str(lineNumber) + ": \"" + str(blockCoordinates[1]) + "\" is an invalid coordinate value. Block coordinate values must be integers in the range [0-31].")
					exit()
				if not checkCoordinate(blockCoordinates[2]):
					print("BlockCoordinateError on Line " + str(lineNumber) + ": \"" + str(blockCoordinates[2]) + "\" is an invalid coordinate value. Block coordinate values must be integers in the range [0-31].")
					exit()
				if not checkCoordinateFit(blockCoordinates,STRUCT_SIZE):
					print("BlockCoordinateOutOfRangeError on Line " + str(lineNumber) + ": \"" + str(blockCoordinates) + "\" is an invalid block coordinate. Block coordinate values must be less than the structure size.")
					exit()
				command = ""
				for x in range(8,len(lineText)):
					command += lineText[x] + " "
				blockData = [blockType,blockDirection,conditional,blockCoordinates,command]
				BLOCK_LIST.append(blockData)
			elif lineText[1] == "line":
				#line code
				print("Not functional yet")
		else:
			print(lineText)
		line = mcsFile.readline()
		lineNumber += 1

	mcsFile.close()
	print("File Successfully Parsed")
	fileData = [STRUCT_SIZE,STRUCT_NAME,BLOCK_LIST,LINE_LIST]
	return fileData


def main():
	fileName = str(input("Enter the name of the MCS file: "))
	if ".mcs" not in fileName[len(fileName)-4:]:
		print("InvalidFileNameError: \"" + str(fileName) + "\" was not an MCS file.")
		exit()
	makeNBTFile(parseFile(fileName))

if __name__ == "__main__":
	main()
