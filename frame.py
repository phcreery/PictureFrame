# Peytons Python Instagram scrapper
# Made for Raspberry pi and 3.2 Waveshare tft LCD
# 
from __future__ import division
import os
import pygame
import time
import sys
from time import gmtime, strftime
import urllib2
import json
import datetime
from InstagramAPI import InstagramAPI
from roundrects import round_rect
#from pygame import *
#from __future__ import division

os.environ["SDL_FBDEV"] = "/dev/fb1"
# Uncomment if you have a touch panel and find the X value for your device
os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ["SDL_MOUSEDEV"] = "/dev/input/event0"

qty=12		#num pics to load per page =qty/2
delay=20	#seconds


print "Peyton's picture frame v1.0"
print "Getting args..."


try:
	print sys.argv[1]
	if sys.argv[1]=="offline":
		print "Offline Mode"
		network=False
	else:
		network=True
except:
	network=True

print "Got Args"

print "Defining Directories and Commands..."
#network=False	#Internet Connection?

refresh=False	#scrap new pictures   for debug

qty2=qty/2
dir="/home/pi/python/picframe/"

os.system("cd "+dir)
#os.system("cd "+dir+"pics")

print "Setting up PyGame..."

fullscreen=False
#bgcolor=255,255,255
bgcolor=220,220,220
fontcolor=0,0,0
fontred=200,80,80
fontgreen=0,160,87
boxcolor=239,224,210

width=320
height=240

mousex=0
mousey=0

print "Initiating Pygame..."
pygame.init()
print pygame.display.Info()
print "Pygame Initiated"
pygame.font.init()
myfont = pygame.font.Font(None, 30)
#myfont2= pygame.font.Font("Roboto-Thin.ttf", 30)
screen = pygame.display.set_mode((width,height))
screen.fill((bgcolor))

if fullscreen==True:
	pygame.display.toggle_fullscreen()
print "Fullscreen Toggled"
pygame.display.flip()
print "Display Refreshed"
#pygame.scrap.init()
pygame.mouse.set_visible(False)
#pygame.scrap.init()
#pygame.scrap.put ("text/plain", str(w))

print "Pygame Setup Complete"

####################################################################



def loadpics():
	global piclist,bgcolor,myfont,screen,qty
	screen.fill((bgcolor))
	myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
	screen.blit((myfont.render("Loading Images",1,fontcolor)),(20,100))
	pygame.display.flip()
	i=0
	piclist = []
	list2 = range(50)
	#while i<qty2:
	#print "Attemting to import "+str(qty2)+" pictures"
	print "Importing all pictures downloaded..."
	success = True
	while success:
		try:
			#i=i+1
			print "Importing pic "+str(i)+".jpg"
			img=pygame.image.load('pics/'+str(i)+'.jpg')
			piclist.append(img)
			i=i+1
			round_rect(screen, (10,210,300,20), (190,190,190),10,0)
			round_rect(screen, (10,210, 250/qty*i+14 ,20), (255,75,75),10,0)
			pygame.display.flip()
		except:
			success=False
			print "Done Importing"
			round_rect(screen, (10,210,300,20), (190,190,190),10,0)
                        round_rect(screen, (10,210,300,20), (255,75,75),10,0)
                        pygame.display.flip()
			time.sleep(1)
			pass


#def statbar():




def newpic2():		#  Centering & filling & correct aspect ratio
	global img
        print "Loading image: ",img
	#img=pygame.image.load('pics/2.jpg')
        #time.sleep(1)
        #print "getting dimensions..."
        newwidth=0
        newheight=0
        width = img.get_width()
        height = img.get_height()
        #print "old: ",width, height
        if (width*0.75 > height):                       #land
                newwidth=240*(float(width)/height)
                newheight=240
                #img = pygame.transform.scale(img, (320, height*(320/width)))
        elif (width*0.75 < height):                     #vert
                newwidth=320
                newheight=320*(float(height)/width)
                #img = pygame.transform.scale(img, (width*(240/height), 240))
        #img = pygame.transform.scale(img, (320, 240))
        #print "convertion: ", width, height, width*0.75, height*0.75, width-320, height-240, height/float(width)
        #print "new: ", newwidth, newheight
        img = pygame.transform.smoothscale(img, (int(newwidth),int(newheight)))
        screen.blit(img,((320-newwidth)/2,(240-newheight)/2))
        #print "blitted"



def mouse():
	global mousex
	global mousey
	pygame.event.get()
	oldmousex=mousex
	oldmousey=mousey
	mousex,mousey = pygame.mouse.get_pos()
	if (mousex<100 and mousex>1) and (oldmousex != mousex):
		print "Left"
	elif (mousex>240) and (oldmousex != mousex):
		print "Right"
	elif (mousex>100 and mousex<240) and (oldmousex != mousex):
		print "Center"
		round_rect(screen, (10,10,10,10), (200,75,75),5,0)
		pygame.display.flip()
		while mousex<240:
			time.sleep(0.05)
			pygame.event.get()
			mousex,mousey = pygame.mouse.get_pos()
		round_rect(screen, (10,10,10,10), (75,200,75),5,0)
		pygame.display.flip()
		#sys.exit()


loadpics()

run=True
while run:

	pygame.display.flip()
	screen.fill((bgcolor))	
	for img in piclist:
		newpic2()
		#status()
		pygame.display.flip()
		#time.sleep(delay)
		mouse()
		end_time = time.time() + delay
		while time.time() < end_time:
			#print "Evaluate certain conditions and display output"
			time.sleep(0.01)
			#print "Checking..."
			mouse()
		
	pygame.display.flip()
	
	print "loop"
	#time.sleep(2)
	
	#api = InstagramAPI("peyton_creery", "Twinsrock98")
	#api.login()

	# user_id = '1461295173'
	#user_id = api.username_id
	
	# List of all followers
	#followers = getTotalFollowers(api, user_id)
	#print 'Number of followers:', len(followers)
	
	# Alternatively, use the code below
	# (check evaluation.evaluate_user_followers for further details).
	#followers = api.getTotalFollowers(user_id)
	#print('Number of followers:', len(followers))
	
