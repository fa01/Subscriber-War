#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################LICENCE####################################
#Copyright (c) 2016 Faissal Bensefia
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
################################################################################
import requests
import json
import curses
#Read in the API key from api_key.txt
try:
	with open("apiKey.txt","r") as file:
		APIKEY=file.readline().strip()
		if len(APIKEY)==0:
			print("Please place your YouTube API key in api_key.txt")
			exit()
except FileNotFoundError:
	open("apiKey.txt","w").close()
	print("Please place your YouTube API key in api_key.txt")
	exit()

#Aquires the number of subscribers a given channelID has
def getSubs(channelID):
    lastRequest = requests.get(
    	"https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+
    	channelID+"&key="+APIKEY)
    return int(json.loads(lastRequest.text)["items"][0]["statistics"]["subscriberCount"])

playerList=[]
playerNames=[]
playerSubCounts=[]
playerColors=[]

#Adds a user to be tracked
def addUser(displayName, channelID,color):
    global playerNames
    global playerList
    global playerSubCounts
    global playerColors
    playerNames.append(displayName)
    playerList.append(channelID)
    playerColors.append(color)
    playerSubCounts.append(0)

addUser("👊 PewDiePie","UC-lHJZR3Gqxm24_Vd_AJ5Yw",curses.COLOR_CYAN+1)
addUser("M Markiplier","UC7_YxT-KID8kRbqZo7MyscQ",curses.COLOR_RED+1)
addUser("👁 JackSepticEye","UCYzPXprvl5Y-Sf0g4vX-m6g",curses.COLOR_GREEN+1)

#Screen initialisation
stdscr=curses.initscr()
curses.start_color()
curses.noecho()
stdscr.nodelay(1)
curses.curs_set(0)
curses.use_default_colors()
for i in range(0, curses.COLORS):
    curses.init_pair(i+1, i, curses.COLOR_WHITE)
RED_ON_WHITE=16
curses.init_pair(RED_ON_WHITE, curses.COLOR_RED, curses.COLOR_WHITE)
WHITE_BG=15
curses.init_pair(WHITE_BG, -1, curses.COLOR_WHITE)
upperPadding=10

term_height, term_width=stdscr.getmaxyx()
#Banner
stdscr.bkgdset(" ", curses.color_pair(WHITE_BG))
stdscr.clear()
stdscr.attron(curses.color_pair(curses.COLOR_RED+1))
stdscr.addstr(1,18,"▗███████████████████████▖")
stdscr.attron(curses.color_pair(RED_ON_WHITE))
stdscr.addstr(2,18,"█     ███████ ██████   ██")
stdscr.addstr(3,18,"███ ███ ███ █ █████ ███ █")
stdscr.addstr(4,18,"███ ███ ███ █    ██     █")
stdscr.addstr(5,18,"███ ███ ███ █ ███ █ █████")
stdscr.addstr(6,18,"███ ████   ███   ███    █")
stdscr.attron(curses.color_pair(curses.COLOR_RED+1))
stdscr.addstr(7,18,"▝███████████████████████▘")
stdscr.attroff(curses.color_pair(curses.COLOR_RED+1))
stdscr.attron(curses.color_pair(1))
stdscr.addstr(2,1,"█   █           ")
stdscr.addstr(3,1," █ █   ███  █  █")
stdscr.addstr(4,1,"  █   █   █ █  █")
stdscr.addstr(5,1,"  █   █   █ █  █")
stdscr.addstr(6,1,"  █    ███   ██")
stdscr.addstr(8,14,"Subscriber War")
for i in range(len(playerNames)):
	#Draw usernames
        stdscr.addstr(upperPadding+(i*3),1,playerNames[i]+":",curses.color_pair(playerColors[i]))

while True:
    #Refresh sub counts
    for i in range(len(playerList)):
        try:
            playerSubCounts[i]=getSubs(playerList[i])
        except:
            pass #If we can't get subcount at this time we'll just leave the value as it is
    margin=len(str(max(playerSubCounts)))+2
    for i in range(len(playerNames)):
        #Clear the line before we write anything
        curses.setsyx(upperPadding+(i*3)+1,0)
        stdscr.clrtoeol()
        
        stdscr.attron(curses.color_pair(playerColors[i]))
        #Subcount
        stdscr.addstr(upperPadding+(i*3)+1,1,str(playerSubCounts[i]))
	
	#Bar
        for ii in range(round(((term_width*4)/(1+(max(playerSubCounts)-playerSubCounts[i])/
        	(max(playerSubCounts)-min(playerSubCounts))))/8)):
            stdscr.addstr(upperPadding+(i*3)+1,margin+ii+1,"█")
	#The fraction of the block at the end if needed
        stdscr.addstr(upperPadding+(i*3)+1,margin+ii+2, chr(ord("█")+int(((term_width*4)/
        	(1+(max(playerSubCounts)-playerSubCounts[i])/(max(playerSubCounts)-min(
        	playerSubCounts))))%8)))
    stdscr.refresh()
endwin()
