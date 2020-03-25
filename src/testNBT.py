nbtPath = '../lib/NBT'
import sys
sys.path.append(nbtPath+'/nbt')
import nbt
from nbt import *

nbtfile = NBTFile()

sizeList = TAG_List(name="size", type=TAG_Int)
sizeList.tags.append(TAG_Int(2))
sizeList.tags.append(TAG_Int(1))
sizeList.tags.append(TAG_Int(1))

entitiesList = TAG_List(name="entities", type=TAG_Compound)


blocksList = TAG_List(name="blocks", type=TAG_Compound)
blocksList.tags.append(TAG_Compound()) #command block

blocksList[0].tags.append(TAG_Compound(name="nbt"))
blocksList[0]["nbt"].tags.append(TAG_Byte(name="conditionMet", value=0))
blocksList[0]["nbt"].tags.append(TAG_Byte(name="auto", value=0))
blocksList[0]["nbt"].tags.append(TAG_String(name="CustomName", value="{\"text\":\"@\"}"))
blocksList[0]["nbt"].tags.append(TAG_Byte(name="powered", value=0))
blocksList[0]["nbt"].tags.append(TAG_String(name="Command", value="say hi"))
blocksList[0]["nbt"].tags.append(TAG_String(name="id", value="minecraft:command_block"))
blocksList[0]["nbt"].tags.append(TAG_Int(name="SuccessCount", value=0))
blocksList[0]["nbt"].tags.append(TAG_Byte(name="TrackOutput", value=1))
blocksList[0]["nbt"].tags.append(TAG_Byte(name="UpdateLastExecution", value=1))

blocksList[0].tags.append(TAG_List(name="pos", type=TAG_Int))
blocksList[0]["pos"].tags.append(TAG_Int(1))
blocksList[0]["pos"].tags.append(TAG_Int(0))
blocksList[0]["pos"].tags.append(TAG_Int(0))

blocksList[0].tags.append(TAG_Int(name="state", value=0))

blocksList.tags.append(TAG_Compound()) #air block

blocksList[1].tags.append(TAG_List(name="pos", type=TAG_Int))
blocksList[1]["pos"].tags.append(TAG_Int(0))
blocksList[1]["pos"].tags.append(TAG_Int(0))
blocksList[1]["pos"].tags.append(TAG_Int(0))

blocksList[1].tags.append(TAG_Int(name="state", value=1))


paletteList = TAG_List(name="palette", type=TAG_Compound)
paletteList.tags.append(TAG_Compound()) #command block

paletteList[0].tags.append(TAG_Compound(name="Properties"))
paletteList[0]["Properties"].tags.append(TAG_String(name="conditional", value="false"))
paletteList[0]["Properties"].tags.append(TAG_String(name="facing", value="west"))
paletteList[0].tags.append(TAG_String(name="Name", value="minecraft:command_block"))

paletteList.tags.append(TAG_Compound()) #air block
paletteList[1].tags.append(TAG_String(name="Name", value="minecraft:air"))

dataVer = TAG_Int(name="DataVersion", value=2230)


nbtfile.tags.append(sizeList)
nbtfile.tags.append(entitiesList)
nbtfile.tags.append(blocksList)
nbtfile.tags.append(paletteList)
nbtfile.tags.append(dataVer)

# print(nbtfile.pretty_tree())
nbtfile.write_file("test.nbt")
print("nbt file made")