#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:16:41 2024

@author: adriandominguezcastro
"""

# Import the required module for text to speech conversion
from gtts import gTTS

# This module is imported so that we can play the converted audio
import os

# The text that you want to convert to audio
mytext = 'May the Force be with you.!'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named audio.mp3
myobj.save("audio.mp3")

# Playing the converted file
# The code uses the command 'open' for macOS
os.system("open audio.mp3")


