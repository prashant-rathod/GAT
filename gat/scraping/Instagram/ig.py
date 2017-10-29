import os
import subprocess

#everything scraped is downloaded to directory folder named after the account you want to scrape
#media is stored here as well as json from metadata
class IGscrape(object):
	def __init__(self, username, password):
		self.name = username
		self.pw = password
	#latest just downloads most recent media since last scrape on this person
	#downloads all pictures/stories/videos 
	def downloadAllMedia(self, account, latest =False):
		if latest == True:
			commandline = "instagram-scraper "+ account +  " --latest" + ' --media-metadata' +" -u "+self.name+ " -p"+ self.pw
			os.system(commandline)
		else:
			commandline = "instagram-scraper "+ account + ' --media-metadata' + " -u "+self.name+ " -p"+ self.pw
			os.system(commandline)
	# Specify media types to scrape. Enter as space separated values. 
    #Valid values are image, video, story, or none. Input as string
	def downloadSpecific(self, account, mediaType):
		commandline = "instagram-scraper "+ account +" -t "+" mediaType" +-" u "+self.name+ " -p "+ self.pw 
	#only download metadate which is a json with links to photos as well as other relevant data including most recent comments and total likes/comments
	#for some reason not working
	def downloadMetaData(self, account):
		commandline = "instagram-scraper "+ account+" --media-metadata -t none" + " -u "+self.name+ " -p "+ self.pw
		os.system(commandline)

	def downloadByHashtag(self, hashtag, maximum = 1000):
		commandline = "instagram-scraper " + "--tag " + hashtag +" -m "+ str(maximum) + " --media-metadata" + " -u " + self.name + " -p " + self.pw
		os.system(commandline)

#this os call doesnt work as intended or same as when you actually put it into command line
#subprocess.call(['instagram-scraper', 'northernlion_gaming', '--media_metadata', '-t', 'none'])





