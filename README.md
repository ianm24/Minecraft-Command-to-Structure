# Minecraft Command-to-Structure

The idea of this project is to make an easy way to make a large command block chain that is easy to edit. 

This project is coded in Python 3.8.1

Thanks to the creaters of the NBT repo, their library made this task much more doable. You can find there repo here: https://github.com/twoolie/NBT
I did make a slight modification to their nbt.py to add the ability to name TAG_Compound but everything else is their work.

## Installation Instructions

Find the directory you would like to put the repository and run `git clone https://github.com/ianm24/Minecraft-Command-to-Structure.git`.
Then run `cd Minecraft-Command-to-Structure/lib` to change directory to the libraries.
Lastly run `git clone https://github.com/ianm24/NBT.git` to get the modified NBT library

## Running Instructions

The MCS file must be in the `input/` directory

Open a command line in the `src/` run `python MCStoNBT.py` then enter the name of your MCS file (for the test file it would be "simpleTest.mcs")

The MCS file format will be converted into an NBT structure file in the `output/` directory. This file will be put into the `world_name/generated/minecraft/structures` folder in your Minecraft Java files then loaded via a structure block. If these directories are not there, you can add them. When loading the structure in Minecraft, remember that the title will be the lowercase version of the title of the generated NBT file.

## Finishing Notes

The specification of the MCS file format is stated in the MCSFormat.txt file.

Note that all chain command blocks are set to always active by default and all other types are set to needs redstone.

The commits through 20 March 2020 were made with a windows git bash that had not had a user name set up, so it appears as committed by "BuilderTools" instead of "ianm24".

If there are any issues with the program itself or the stated file format please feel free to add it using the GitHub issue tracker.
