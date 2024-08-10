# Text to Speech Conversion

This Python code demonstrates how to convert a given text into speech using the gTTS (Google Text-to-Speech) library and then plays the converted audio file. 

### Features

* **Text to Speech Conversion:** Converts the provided text into audio using Google Text-to-Speech.

* **Language Support:** Supports multiple languages for conversion.

* **Speed Control:** Option to convert the text to speech at normal speed.

* **Audio Playback:** Automatically plays the converted audio file after saving.



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

 * Python 3.8.3
 * gTTS library
 * Operating system with a command to play audio files (e.g., open for macOS)

### Installation

To run this code, you need to install the required gTTS library. You can install it using pip:
```bash
pip install gTTS
```

