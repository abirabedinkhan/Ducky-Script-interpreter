import time 
import pyautogui
import keyboard
import sys
import os
import requests

try:
	duckyScriptPath = sys.argv[1]
except:
	duckyScriptPath = 'payload.dd'

f = open(duckyScriptPath,"r",encoding='utf-8')
duckyScript = f.readlines()
duckyScript = [x.strip() for x in duckyScript] 

defaultDelay = 0
if duckyScript[0][:7] == "DEFAULT":
	defaultDelay = int(duckyScript[0][:13]) / 1000
	
duckyCommands = [
"WINDOWS", "GUI", "APP", "MENU", "SHIFT", "ALT", "CONTROL", "CTRL", "DOWNARROW", "DOWN",
"LEFTARROW", "LEFT", "RIGHTARROW", "RIGHT", "UPARROW", "UP", "BREAK", "PAUSE", "CAPSLOCK", "DELETE", "END",
"ESC", "ESCAPE", "HOME", "INSERT", "NUMLOCK", "PAGEUP", "PAGEDOWN", "PRINTSCREEN", "SCROLLLOCK", "SPACE", 
"TAB", "ENTER", " a", " b", " c", " d", " e", " f", " g", " h", " i", " j", " k", " l", " m", " n", " o", " p", " q", " r", " s", " t",
" u", " v", " w", " x", " y", " z", " A", " B", " C", " D", " E", " F", " G", " H", " I", " J", " K", " L", " M", " N", " O", " P",
" Q", " R", " S", " T", " U", " V", " W", " X", " Y", " Z"
]

keyboardCommands = [
"win", "win", "win", "win", "shift", "alt", "ctrl", "ctrl", "down", "down",
"left", "left", "right", "right", "up", "up", "pause", "pause", "capslock", "delete", "end",
"esc", "escape", "home", "insert", "numlock", "pageup", "pagedown", "printscreen", "scrolllock", "space",
"tab", "enter", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
"u", "v", "w", "x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
"q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

def lex(line, prev):

	# Variables:
	data = []	

	# Check if the statement is a delay
	if line[0:5] == "DELAY" :
		time.sleep(float(line[6:]) / 1000)
	
	elif line[0:4] == "PATH":
		if line[5:].startswith('https://'):
			try:
				webScipts = requests.get(line[5:]).text
			except:
				webScipts = 'REM'
				print('Please check your internet connection!')
			duckyScript = webScipts.split('\n')
		else:
			duckyScriptPath = line[5:]
			f = open(duckyScriptPath,"r",encoding='utf-8')
			duckyScript = f.readlines()
			duckyScript = [x.strip() for x in duckyScript] 

		prev = ''

		for line in duckyScript:
			lex(line, prev)
			previous = line
			prev = previous

	elif line[0:2] == 'OS':
		os.system(line[3:])

	elif line[0:6] == "STRING" :
		pyautogui.typewrite(line[7:], interval=0.02)

	elif line[0:6] == "REPEAT" :
		for i in range(int(line[7:]) - 1):
			lex(prev, prev)

	elif line[0:3] == "REM":
		line.replace("REM", "#")
		
	elif line == '' or line == None:
		line = 'REM'

	else:
		for j in range(len(keyboardCommands)):
			if line.find(duckyCommands[j]) != -1:
				data.append(keyboardCommands[j])
		keyboard.press_and_release('+'.join(data))
		data = []

		# Write Default Delay if it exists:
		if defaultDelay != 0:
			time.sleep(defaultDelay)

prev = ''

for line in duckyScript:
	lex(line, prev)
	previous = line 
	prev = previous	
