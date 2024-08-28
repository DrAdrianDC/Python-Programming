#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 05:14:51 2024

@author: adriandominguezcastro
"""

# Import the required module for text to speech conversion
from gtts import gTTS

# Import the module to extract text from a PDF file
import PyPDF2

# Import the Translator module from googletrans to translate text
from googletrans import Translator

# This module is imported so that we can play the converted audio
import os

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    # Open the PDF file in binary mode
    with open(pdf_file, 'rb') as file:
        # Initialize a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty string to store the extracted text
        text = ""
        
        # Iterate through all the pages and extract text
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text

# Path to the PDF file
pdf_file = 'sample.pdf'

# Extract text from the PDF file
mytext = extract_text_from_pdf(pdf_file)

# Initialize the Translator object
translator = Translator()

# Translate the extracted text from English to Spanish
translated_text = translator.translate(mytext, src='en', dest='es').text

# Language in which you want to convert the translated text
language = 'es'

# Passing the translated text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should have a high speed
myobj = gTTS(text=translated_text, lang=language, slow=False)

# Saving the converted audio in a mp3 file named audio.mp3
myobj.save("translated-audio.mp3")

# Playing the converted file
# The code uses the command 'open' for macOS
os.system("open translated-audio.mp3")
