# Text-to-Speech (TTS) using Python


This repository contains a collection of Python programs that demonstrate different approaches to converting text to speech (TTS). These programs showcase how to generate audio from text embedded directly in the code, extract text from a PDF file and convert it to audio, and even translate text from English to Spanish before converting it to audio.


## Table of Contents

- [Project Structure](#project-structure)
- [Programs Overview](#programs-overview)
  - [1. Embedded Text-to-Audio](#1-embedded-text-to-audio)
  - [2. PDF Text Extraction and Audio Conversion](#2-pdf-text-extraction-and-audio-conversion)
  - [3. English-to-Spanish Translation and Audio Conversion](#3-english-to-spanish-translation-and-audio-conversion)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Project Structure

Each folder contains a Python program that performs a specific text-to-audio conversion task.

## Programs Overview

### 1. Embedded Text-to-Audio

This program generates audio from text that is directly embedded in the Python code. It uses a text-to-speech (TTS) engine to convert the text into spoken words.

**Features:**
- Simple and straightforward text-to-audio conversion.
- Ideal for generating audio from predefined texts.

### 2. PDF Text Extraction and Audio Conversion

This program extracts text from a PDF file and then converts it into audio. It can handle multi-page PDFs and convert the extracted text into spoken words.

**Features:**
- Extracts text from PDF files.
- Converts extracted text to audio.

### 3. English-to-Spanish Translation and Audio Conversion

This program first translates English text into Spanish and then converts the translated text into audio. It's useful for creating bilingual audio content.

**Features:**
- Translates English text to Spanish.
- Converts translated text to audio.



--------------------------------------------
**1.- Text in Code to Audio**

This Python code demonstrates how to convert a given text into speech using the gTTS (Google Text-to-Speech) library and then plays the converted audio file.




### How to usage

**Modify the Text:** Change the value of mytext in the script to the text you want to convert to speech.

**Set the Language:** Set the language variable to the desired language code (e.g., 'en' for English).    

 **Run the Program**: Execute the code to convert the text to speech and save it as an mp3 file.
```bash
./python text-to-speech.py
```
or

```bash
python text-to-speech.py
```

**Play the Audio:** The script will automatically play the saved audio file.



## Requirements

Ensure you have the following Python packages installed:

- `gTTS` (Google Text-to-Speech)
- `PyPDF2` (for PDF text extraction)
- `googletrans` (for text translation)
- Other common packages like `os` and `sys`

You can install the required packages using pip:

```bash
pip install gtts PyPDF2 googletrans==4.0.0-rc1



