# Copyright 2020 Ian McDowell
nbtPath = '../lib/NBT'
inputPath = '../input/'
outputPath = '../output/'
import sys
import copy
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
def checkLineDirection(lineDirection,lineStartCoordinates):
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

# Makes sure the snake wont go outside of the structure
def checkSnakeLineLimit(startCoords,startDirection,lineLimit):
	return startCoords[getDirectionValue(startDirection)[0]] + lineLimit-1 < 32

# Makes sure the snake static dimension is valid
def checkSnakeStaticDimension(staticDimensionChar):
	return staticDimensionChar in ['x','y','z']

# Makes sure the snake sign is valid
def checkSnakeSign(sign):
	return sign in ["pos","neg"]

# Makes sure the snake direction doesnt conflict with the static dimension
def checkSnakeStaticWithDirection(snakeStaticDimension,snakeDirection):
	return not getDimensionValue(snakeStaticDimension) == getDirectionValue(snakeDirection)[0]

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

# Returns the list position of a dimension
def getDimensionValue(dimension):
	if dimension == 'x':
		return 0
	elif dimension == 'y':
		return 1
	elif dimension == 'z':
		return 2

# Returns integer with inputted sign
def getSignValue(sign):
	if sign == "pos":
		return 1
	elif sign == "neg":
		return -1
	else:
		return False

# Returns other dimension being used in snake
def getOtherDimension(currCoord,direction,staticDimension):
	tempCoord = currCoord[:]
	tempCoord[direction[0]] += direction[1]
	for x in range(0,3):
		if x == staticDimension:
			continue
		if not tempCoord[x] - currCoord[x] == direction[1]:
			return x

# Converts the file's block type to the NBT compatible type
def getFinalizedBlockType(blockType):
	if blockType == "repeating":
		return "repeating_command_block"
	elif blockType == "chain":
		return "chain_command_block"
	elif blockType == "impulse":
		return "command_block"
	else:
		return False

# Given block data, validates input and returns data as list
def makeBlock(blockType,blockDirection,conditional,blockCoordinates,command,lineNumber,usedCoordList):
	if not checkBlockType(blockType):
		print("BlockTypeError on Line " + str(lineNumber) + ": \"" + str(blockType) +
			"\" is not a valid block type. Block types must be either \"repeating\",\"chain\", or \"impulse\".")
		exit()
	modifiedBlockType = getFinalizedBlockType(blockType)
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
	return [modifiedBlockType,blockDirection,conditional,blockCoordinates,command]

# Returns the next snake block's coordinates and direction
def getNextSnakeBlock(startCoords,currCoord,lineLimit,direction,staticDimensionChar,otherDimDirection):
	startDirection = getDirectionName(direction)
	staticDimension = getDimensionValue(staticDimensionChar)
	sign = getSignValue(otherDimDirection)
	otherDimension = getOtherDimension(currCoord,direction,staticDimension)
	otherDirection = [otherDimension,sign]

	# Figures out if the snake is going towards or away from the tail
	directionSwap = currCoord[otherDirection[0]] - startCoords[otherDirection[0]]
	if directionSwap % 2 == 1:
		direction[1] *= -1
	lineLimitTest = currCoord[direction[0]] + direction[1] - startCoords[direction[0]]

	# If the snake is at the end of a line
	if lineLimitTest > lineLimit-1:
		direction[1] *= -1
		currCoord[otherDirection[0]] += otherDirection[1]
		return [currCoord,getDirectionName(direction)]
	elif lineLimitTest < 0:
		direction[1] *= -1
		currCoord[otherDirection[0]] += otherDirection[1]
		return [currCoord,getDirectionName(direction)]
	# If the snake is about to be at the end of a line
	elif lineLimitTest == lineLimit-1:
		currCoord[direction[0]] += direction[1]
		return [currCoord, getDirectionName(otherDirection)]
	elif lineLimitTest == 0:
		currCoord[direction[0]] += direction[1]
		direction[1] *= -1
		return [currCoord, getDirectionName(otherDirection)]
	# If the snake is in the middle of a line
	elif lineLimitTest < lineLimit-1:
		currCoord[direction[0]] += direction[1]	
		if directionSwap % 2 == 1:
			return [currCoord,getDirectionName(direction)]
		else:
			return[currCoord,startDirection]

# Gets the current state's position in the state list
def getState(currState, stateList):
	for x in range(0,len(stateList)):
		if currState == stateList[x]:
			return x
	return len(stateList)


# Uses file data from parseFile() to create the structure's NBT file
def makeNBTFile(fileData):
	STRUCT_INFO = fileData[0]
	BLOCK_LIST = fileData[1]
	USED_COORDS_LIST = fileData[2]
	AIR_BLOCKS = []

	print("Writing " + outputPath + STRUCT_INFO[1] + ".nbt")
	
	nbtfile = NBTFile()
	sizeList = TAG_List(name="size", type=TAG_Int)
	sizeList.tags.append(TAG_Int(STRUCT_INFO[0][0]))
	sizeList.tags.append(TAG_Int(STRUCT_INFO[0][1]))
	sizeList.tags.append(TAG_Int(STRUCT_INFO[0][2]))

	entitiesList = TAG_List(name="entities", type=TAG_Compound)
	blocksList = TAG_List(name="blocks", type=TAG_Compound)
	paletteList = TAG_List(name="palette", type=TAG_Compound)

	stateList = []

	for x in range(0,len(BLOCK_LIST)):
		currState = [BLOCK_LIST[x][0],BLOCK_LIST[x][2],BLOCK_LIST[x][1]]
		autoVal = 0
		if currState[0] == "chain_command_block":
			autoVal = 1

		blocksList.tags.append(TAG_Compound())
		blocksList[x].tags.append(TAG_Compound(name="nbt"))
		blocksList[x]["nbt"].tags.append(TAG_Byte(name="conditionMet", value=0))
		blocksList[x]["nbt"].tags.append(TAG_Byte(name="auto", value=autoVal))
		blocksList[x]["nbt"].tags.append(TAG_String(name="CustomName", value="{\"text\":\"@\"}"))
		blocksList[x]["nbt"].tags.append(TAG_Byte(name="powered", value=0))
		blocksList[x]["nbt"].tags.append(TAG_String(name="Command", value=BLOCK_LIST[x][4]))
		blocksList[x]["nbt"].tags.append(TAG_String(name="id", value="minecraft:command_block"))
		blocksList[x]["nbt"].tags.append(TAG_Int(name="SuccessCount", value=0))
		blocksList[x]["nbt"].tags.append(TAG_Byte(name="TrackOutput", value=1))
		blocksList[x]["nbt"].tags.append(TAG_Byte(name="UpdateLastExecution", value=1))
		blocksList[x].tags.append(TAG_List(name="pos", type=TAG_Int))
		blocksList[x]["pos"].tags.append(TAG_Int(BLOCK_LIST[x][3][0]))
		blocksList[x]["pos"].tags.append(TAG_Int(BLOCK_LIST[x][3][1]))
		blocksList[x]["pos"].tags.append(TAG_Int(BLOCK_LIST[x][3][2]))
		blocksList[x].tags.append(TAG_Int(name="state", value=getState(currState,stateList)))

		if not currState in stateList:
			paletteList.tags.append(TAG_Compound())
			paletteList[len(stateList)].tags.append(TAG_Compound(name="Properties"))
			paletteList[len(stateList)]["Properties"].tags.append(TAG_String(name="conditional", value=BLOCK_LIST[x][2]))
			paletteList[len(stateList)]["Properties"].tags.append(TAG_String(name="facing", value=BLOCK_LIST[x][1]))
			paletteList[len(stateList)].tags.append(TAG_String(name="Name", value="minecraft:"+BLOCK_LIST[x][0]))
			stateList.append(currState[:])

	amountOfAirBlocks = 0
	for x in range(0,STRUCT_INFO[0][0]):
		for y in range(0,STRUCT_INFO[0][1]):
			for z in range(0,STRUCT_INFO[0][2]):
				if not [x,y,z] in USED_COORDS_LIST:
					blocksList.tags.append(TAG_Compound())
					blocksList[len(BLOCK_LIST)+amountOfAirBlocks].tags.append(TAG_List(name="pos", type=TAG_Int))
					blocksList[len(BLOCK_LIST)+amountOfAirBlocks]["pos"].tags.append(TAG_Int(x))
					blocksList[len(BLOCK_LIST)+amountOfAirBlocks]["pos"].tags.append(TAG_Int(y))
					blocksList[len(BLOCK_LIST)+amountOfAirBlocks]["pos"].tags.append(TAG_Int(z))
					blocksList[len(BLOCK_LIST)+amountOfAirBlocks].tags.append(TAG_Int(name="state", value=len(stateList)))
					amountOfAirBlocks += 1

	paletteList.tags.append(TAG_Compound())
	paletteList[len(stateList)].tags.append(TAG_String(name="Name", value="minecraft:air"))


	dataVer = TAG_Int(name="DataVersion", value=2230)

	nbtfile.tags.append(sizeList)
	nbtfile.tags.append(entitiesList)
	nbtfile.tags.append(blocksList)
	nbtfile.tags.append(paletteList)
	nbtfile.tags.append(dataVer)
	
	# print(nbtfile.pretty_tree())
	nbtfile.write_file(outputPath + STRUCT_INFO[1] + ".nbt")

	print(outputPath + STRUCT_INFO[1] + ".nbt Successfully Written")

# Parses the MCS file and returns all relavent file data
def parseFile(fileName):
	print("Parsing " + fileName)
	mcsFile = open(fileName, 'r')
	line = mcsFile.readline()
	lineNumber = 1

	LINE_MODE = False
	SNAKE_MODE = False
	CURR_LENGTH = 0
	CURR_DIRECTION = [-1,-1]
	STRUCT_INFO = [[-1,-1,-1],""]
	BLOCK_LIST = []
	USED_COORDS_LIST = []
	START_COORDINATES = []
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
				START_COORDINATES = []
				CURR_LENGTH = 0
				CURR_DIRECTION = [-1,-1]
				line = mcsFile.readline()
				lineNumber += 1
				continue
			if nextLineBlock[CURR_DIRECTION[0]] >= 32 or nextLineBlock[CURR_DIRECTION[0]] < 0:
				print("LineOutOfBoundsError on Line " + str(lineNumber) + ": \"" + str(nextLineBlock) +
						"\" is outside of the structure. Make sure your line fits inside of the structure.")
				exit()
			blockType = lineText[0]
			conditional = lineText[1]
			command = ""
			for x in range(2,len(lineText)):
				command += lineText[x] + " "
			lineBlockData = makeBlock(blockType,CURR_DIRECTION,conditional,nextLineBlock[:],command,lineNumber,USED_COORDS_LIST)
			USED_COORDS_LIST.append(nextLineBlock[:])
			BLOCK_LIST.append(lineBlockData[:])
			CURR_LENGTH += 1
			nextLineBlock[CURR_DIRECTION[0]] += CURR_DIRECTION[1]

		# Creating Snakes
		elif SNAKE_MODE:
			if lineText[0] ==  '}':
				SNAKE_MODE = False
				START_COORDINATES = []
				CURR_DIRECTION = [-1,-1]
				CURR_LENGTH = 0
				line = mcsFile.readline()
				lineNumber += 1
				continue
			# print(nextSnakeBlock)
			coords = nextSnakeBlock[0][:]
			direction = nextSnakeBlock[1][:]
			if not checkCoordinates(coords):
				print("SnakeOutOfBoundsError on Line " + str(lineNumber) + ": \"" + str(nextSnakeBlock) +
						"\" is outside of the structure. Make sure your snake fits inside of the structure.")
				exit()
			blockType = lineText[0]
			conditional = lineText[1]
			command = ""
			for x in range(2,len(lineText)):
				command += lineText[x] + " "
			snakeBlockData = makeBlock(blockType,direction,conditional,coords[:],command,lineNumber,USED_COORDS_LIST)
			USED_COORDS_LIST.append(coords[:])
			BLOCK_LIST.append(snakeBlockData[:])
			nextSnakeBlock = getNextSnakeBlock(START_COORDINATES[:],coords[:],snakeLineLimit,CURR_DIRECTION[:],snakeStaticDimension,snakeSign)


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
				if not checkLineDirection(lineDirection,lineStartCoordinates):
					print("LineDirectionError on Line " + str(lineNumber) + ": \"" + str(lineDirection) +
						"\" points the line outside of the structure. Remember \"east\" points in the positive X direction," +
						"\"west\" points in the negative X direction, \"up\" points in the positive Y direction,\"down\" points in the negative Y direction," +
						" \"south\" points in the positive Z direction, and \"north\" points in the negative Z direction.") 
					exit()
				LINE_MODE = True
				CURR_DIRECTION = getDirectionValue(lineDirection)
				START_COORDINATES = lineStartCoordinates
				nextLineBlock = [lineStartCoordinates[0],lineStartCoordinates[1],lineStartCoordinates[2]]

			#New Snakes
			elif lineText[1] == "snake":
				snakeStartCoordinates = [int(lineText[2]),int(lineText[3]),int(lineText[4])]
				if not checkCoordinates(snakeStartCoordinates):
					print("SnakeCoordinateOutOfRangeError on Line " + str(lineNumber) + ": \"" + str(snakeStartCoordinates) +
						"\" is an invalid snake start coordinate. Snake start coordinate values must be inside the structure.")
					exit()
				snakeDirection = lineText[6]
				if not checkBlockDirection(snakeDirection):
					print("InvalidDirectionError on Line " + str(lineNumber) + ": \"" + str(snakeDirection) +
						"\" is not a valid direction. Directions must be either \"up\",\"down\",\"north\",\"south\",\"east\", or \"west\".")
					exit()
				if not checkLineDirection(snakeDirection,snakeStartCoordinates):
					print("SnakeDirectionError on Line " + str(lineNumber) + ": \"" + str(snakeDirection) +
						"\" points the snake outside of the structure. Remember \"east\" points in the positive X direction," +
						"\"west\" points in the negative X direction, \"up\" points in the positive Y direction,\"down\" points in the negative Y direction," +
						" \"south\" points in the positive Z direction, and \"north\" points in the negative Z direction.") 
					exit()
				snakeLineLimit = int(lineText[5])
				if not checkSnakeLineLimit(snakeStartCoordinates,snakeDirection,snakeLineLimit):
					print("SnakeLineLimitError on Line " + str(lineNumber) + ": \"" + str(snakeLineLimit) +
						"\" is too large. Snake line limits must keep the snake within the structure.")
					exit()
				snakeStaticDimension = lineText[7]
				if not checkSnakeStaticDimension(snakeStaticDimension):
					print("InvalidStaticDimensionError on Line " + str(lineNumber) + ": \'" + str(snakeStaticDimension) +
						"\' is not a valid dimension. Valid dimensions are \'x\',\'y\', and \'z\'.")
					exit()
				if not checkSnakeStaticWithDirection(snakeStaticDimension,snakeDirection):
					print("ConflictingStaticAndDirectionError on Line " + str(lineNumber) + ": \'" + str(snakeStaticDimension) +
						"\' cannot be static as it is direction moved through. Remember that \"" + str(snakeDirection) + "\" moves in the "
						+ str(['x','y','z'][getDirectionValue(snakeDirection)[0]]) + " dimension.")
					exit()
				snakeSign = lineText[8]
				if not checkSnakeSign(snakeSign):
					print("InvalidSignError on Line " + str(lineNumber) + ": \'" + str(snakeSign) +
						"\' is not a valid sign. Valid signs are \"pos\", and \"neg\".")
					exit()
				SNAKE_MODE = True
				CURR_DIRECTION = getDirectionValue(snakeDirection)
				START_COORDINATES = snakeStartCoordinates
				nextSnakeBlock = [snakeStartCoordinates,snakeDirection]
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
	fileName = inputPath+str(input("Enter the name of the MCS file: "))
	if ".mcs" not in fileName[len(fileName)-4:]:
		print("InvalidFileNameError: \"" + str(fileName) + "\" was not an MCS file.")
		exit()
	makeNBTFile(parseFile(fileName))

if __name__ == "__main__":
	main()
