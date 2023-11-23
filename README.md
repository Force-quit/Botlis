# Botlis

Botlis is a discord bot written in python used for playing music in voice clients. So far only youtube and single channel play are supported.

## Setup
- Use python 3.11.x
- Open in VS Code
- Open terminal and create virtual environment (first time only)
  - on Windows: py -m venv env
  - on Windows (older installations of python): python -m venv env
  - on linux/mac: python -m venv env
- Source your virtual environment (every time you want to issue some command for the project) :
  - on Windows PS: .\env\Scripts\Activate.ps1
  - on Windows CMD: .\env\Scripts\activate.bat
  - on linux/mac: source env/bin/activate
- Install the requirements : pip install -r requirements.txt
- Install ffmpeg.exe and add it to your %PATH% (figure it out).

You're now ready to work on the project

## Features
- `/play [url]` slash command, which takes a youtube URL and plays the audio of the video in the channel that the author of the command was in
- automatic storage management: all assets used by the /play command are managed automatically once the playing stops, this prevents storage from getting destroyed
- bot disconnects once it's done playing
