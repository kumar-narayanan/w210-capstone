W210-Captone

# This directory contains the workflow files - utterance, intent, slots, values etc

# The main file is the Python NB - multiwoz.ipynb.

The way to run the code is to edit the first cell in the NB.
- To change the name of the text file that has utterances use the variable
    utterance_file. You can either provide a full path or keep the file in
    the local directory. 
- The output file name is set to "dialogues_011.json, keeping in line with 
the multiwoz convention. This file be OVERWRITTEN everytime you run. So, if
you want to keep the older outputs please change the file name.
- Other domains list is a list that all the 7 domains other than restaurant
in the multiwoz 2.2 data set.
- Currently, only one active domain is handled - "restaurant"

Format of the utternace file
- You can look at utterance2.txt or utterance_multi.txt
- Begin each worflow with "----". You can add a descriptive test after that.
Ex. 
----query for restaurant timings
- No blank lines at the end. The program is not smart enough to handle that.
- Other the line starting with "----" every other line should start with 
"SYSTEM" or "USER", and follow it up with ':' (colon)
- In square brackets ([]) for "USER" please provide a triplet of slot name,
slot value, and active intent, in that order. These 3 entities MUST be 
comma (,) separated. PLEASE DO NOT EMBED COMMAS INSIDE THESE STRINGS.
- If the dialog is from "SYSTEM" then no need to have entries in the square
brackets. You still need the square bracket but leave it empty - ie. "[]".
- If you want to have slot name and slot values for the "SYSTEM" dialog
please include within the square brackets, comma separated. At least two 
values are needed - the slot name and slot value in that order
- The code searches for the slot value in the utterance. So, it's important
that the slot value you specify can be located in the utterance.

These are the rules from multiwoz. Nothing to do with my imagination.

Please look at the utterance files to get an idea of how to instantiate workflow
utterances,

############Updated 10/12/2022 5:30PM PDT###############
- Added bertgen.ipynb to convert multiwoz to bert data set for only restaurant
domain.
- The input is "dialogues_016.json" in multiwoz format
- Output is "bert_dialogues_016.json

