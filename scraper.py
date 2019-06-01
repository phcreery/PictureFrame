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

qty=10		#num pics to load per page =qty/2
delay=20	#seconds
tag="overland"	#hashtag
getuser="peyton_creery"
#getuser="melissahaileyy,peyton_creery,_huntercreery_,shortstache,petermckinnon,forgeoverland,thelevelcollective,roamtheplanet"
user=True
username="user"
password="pass"

print "Peyton's Instagram scraper v1.0"
print "whats new:"
print "- Automatic network detection"
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
#qty=str(qty)

#print "Attempting to scrap " +str(qty) + " pictures"
dir="/home/pi/python/instapy/myscraper/"
if user==False:
	scrapcommand="instagram-scraper "+tag+" --tag -d pics -m "+str(qty)+" -t image -u "+username+" -p "+password+" -v 1"
else:
	scrapcommand="instagram-scraper "+getuser+" -d pics -m "+str(qty)+" -t image -u "+username+" -p "+password+" -v 1"
mvcommand='i=0;for file in pics/*.jpg ; do mv "$file" "pics/$i.jpg" ; i="$((i+1))"  ; done'
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

def checkinternet():
	global network
	print "Checking Internet Connection"
	screen.fill((bgcolor))
        myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
        screen.blit((myfont.render("Checking Internet",1,fontcolor)),(20,100))
        pygame.display.flip()

	try:
		urllib2.urlopen('http://216.58.192.142', timeout=1)   #googles ip
		network = True
		#screen.fill((bgcolor))
		screen.blit((myfont.render("Connected",1,fontcolor)),(20,130))
	        pygame.display.flip()
		time.sleep(1)
	except urllib2.URLError as err: 
		network = False
		screen.blit((myfont.render("Not Connected",1,fontcolor)),(20,130))
                pygame.display.flip()
                time.sleep(1)


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

	

def newlist():
	#os.system(
	os.system("rm -r pics")
	print "Scrapping..."
	screen.fill((bgcolor))
        myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
        screen.blit((myfont.render("Downloading Images",1,fontcolor)),(20,100))
        pygame.display.flip()
	os.system(scrapcommand) #"instagram-scraper overland --tag -d pics -m 5 -t image -u peyton_creery -p Twinsrock98"
	print "Renaming..."
	screen.fill((bgcolor))
        myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
        screen.blit((myfont.render("Processing Images",1,fontcolor)),(20,100))
        pygame.display.flip()
	os.system(mvcommand)
	#os.system("cd "+dir)



def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    print "Loading Followers..."
    screen.fill((bgcolor))
    myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
    screen.blit((myfont.render("Counting Followers",1,fontcolor)),(20,100))
    pygame.display.flip()
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
	#print "inapp: ", len(followers)
    print "Follower count: ",followers
    return followers


def status():
	global api, user_id,username, followers,network

	myfont = pygame.font.Font(pygame.font.match_font('mono'), 15)
	#myfont = pygame.font.Font(dir+"Roboto-Thin.ttf", 24)
	
	#followers = getTotalFollowers(api, user_id)
	#print "str: ",followers
        #print 'Number of followers:', len(followers)
	
	#pygame.draw.rect(screen, (0,0,0), (0,220,320,20), 0)
	#AAfilledRoundedRect(screen,(0,220,320,20),boxcolor,0.5)
	round_rect(screen, (10,210,300,20), boxcolor, 10,0)
	if network==True:
		screen.blit((myfont.render(username+"   Followers: "+str(len(followers)),1,fontcolor)),(20,212))
	else:
		screen.blit((myfont.render(username+"   Followers: NULL",1,fontcolor)),(20,212))
	#screen.blit(text,(320 - text.get_width() // 2, 240 - text.get_height() // 2))

	
	#print pygame.font.get_fonts()
	
	#image=pygame.image.load("icons/temp.png")
	#screen.blit(image,(100,30))
	
	#pygame.draw.line(screen, (255,0,0), (day*53,-(temphigh/1.5)+125), (day*53+53,-(temphigh/1.5)+125), 2)
	#screen.blit((myfont.render(todayforecast,1,(fontcolor),bgcolor)),(day*53+2,25))
	#pygame.display.flip()
	#time.sleep(5)



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
	mousex,mousey = pygame.mouse.get_pos()
	if (mousex<(180)) and mousex>1:
		print "Exiting..."
		sys.exit()



checkinternet()


if network==True:

	print "Logging in..."
	screen.fill((bgcolor))
	myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
	screen.blit((myfont.render("Logging In...",1,fontcolor)),(20,100))
	pygame.display.flip()
	try:
		api = InstagramAPI("peyton_creery", "Twinsrock98")
		api.login()
		user_id = api.username_id
		#screen.fill((bgcolor))
                myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
                screen.blit((myfont.render("Success",1,fontcolor)),(20,130))
                pygame.display.flip()
		time.sleep(1)
	except:
		#screen.fill((bgcolor))
        	myfont = pygame.font.Font(pygame.font.match_font('mono'), 25)
        	screen.blit((myfont.render("Error",1,fontcolor)),(20,130))
        	pygame.display.flip()
		print "Unable to login"
		time.sleep(1)

#update()
if refresh==True and Network==True:
	newlist()

loadpics()

run=True
while run:
	if network==True:
		followers = getTotalFollowers(api, user_id)
	else:
		followers = 0
        #print 'Number of followers:', len(followers)

	pygame.display.flip()
	screen.fill((bgcolor))	
	for img in piclist:
		newpic2()
		status()
		pygame.display.flip()
		time.sleep(delay)
		
	pygame.display.flip()
	
	print "loop"

