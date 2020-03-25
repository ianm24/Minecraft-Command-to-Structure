# Minecraft Command-to-Structure

The idea of this project is to make an easy way to make a large command block chain that is easy to edit. 
The MCS file format will be converted into an NBT structure file to be put into the `world/generated/structures` folder then loaded via a structure block

Thanks to the creaters of the NBT repo, their library made this task much more doable. You can find there repo here: https://github.com/twoolie/NBT
I did make a slight modification to their nbt.py to add the ability to name TAG_Compound but everything else is their work.