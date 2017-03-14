#!/usr/bin/python3
import re
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import urllib.request as urlRequest
import requests

class crawlUrl(object):

	def __init__(self,urltype,htmlurl):
		self.htmlUrl = htmlurl
		self.urlType = urltype
		self.video_list={}
		self.downloads={}
		self.title_list={}

	def crawlQuery(self):
		req = self.requestUrl(self.htmlUrl)
		dict_link = self.crawlQueryUrl(req)
		return(dict_link)


	def requestUrl(self,htmlUrl):
		req = urllib.request.Request(htmlUrl, headers={'User-Agent': 'Mozilla/5.0'})
		return(req)

	def crawlQueryUrl(self,req,):
		soup = BeautifulSoup(urlopen(req).read(),"html.parser")
		stop_words = (['"', "'",'/'])
		#Parsing web urls
		for item in soup.find_all('h3', attrs={'class' : 'yt-lockup-title'}):

		    link = item.a['href']
		    title = item.a['title']
		    title = [i for i in title if i not in stop_words]
		    title = "".join(title)
		    if self.urlType == 2:
		    	if "&list=" in link:
		    		full_link ="https://www.youtube.com"+link
		    		self.video_list[title]=full_link
		    elif self.urlType == 1:
		    	full_link ="https://www.youmagictube.com"+link
		    	if "&list=" in link:
		    		continue
		    	else:
		    		self.video_list[title]=full_link
		if  self.urlType == 1:
			return (self.video_list)
		elif self.urlType == 2:
			return(self.video_list)

	def selectLink(self,videos_choice):
		choice = self.video_list[videos_choice]
		quality = self.findQuality(choice)
		return(quality)
	def findQuality(self,videoslink):		

		reg=re.compile('[a-zA-Z0-9-_]+$')
		r = reg.search(videoslink).group()

		save="http://www.save-video.com/download.php?s=magicyt&url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D"+r

		req = self.requestUrl(save)

		soup = BeautifulSoup(urlopen(req).read(),"html.parser")

		divs = soup.find('div', attrs={'class' : 'sv-download-links'})
		for item in divs.find_all('li'):
			s=item.a['href']
			self.downloads[str(item.text)]=s

		
		if 'MP3 NEW' in self.downloads.keys():
			del self.downloads['MP3 NEW']

		return (self.downloads)

	def crawlQualitylink(self,quality_choice):
	
		if quality_choice not in self.downloads.keys():
			quality_choice = 'default'
		if quality_choice =='default':
				if 'MP4(480 x 360)' in self.downloads.keys():
					quality_choice = 'MP4(480 x 360)' 
				else:
					quality_choice = next(iter(self.downloads))
		save_video = "http://www.save-video.com/"+self.downloads[quality_choice]+"#"
		url = save_video
		req = self.requestUrl(url)
		self.downloadLink(req)
				
	
	def downloadLink(self,req):
		soup = BeautifulSoup(urlopen(req).read(),"html.parser")
		download_name = (soup.find('div').h1.text).split('"')[1]
		temp1=None
		for item in soup.find_all('h1', attrs={'class' : 'sv-s-download-link start-download'}):
		    temp1=item.a['href']


		for item in soup.find_all('h1', attrs={'class' : 'sv-s-download-link'}):
		    temp2="http://www.save-video.com/"+item.a['href']


		if temp1 == None:
			target = urllib.request.urlretrieve(temp2,download_name)
		else:
			r = requests.get(temp1)
			target = urllib.request.urlretrieve(r.history[0].url,download_name)
		print("downloaded "+download_name)

	def getPlaylist_videos(self,playlist_choice):
		title_list={}
		choice = self.video_list[playlist_choice]
		req = self.requestUrl(choice)
		soup = BeautifulSoup(urlopen(req).read(),"html.parser")
		divs = soup.find('div', attrs={'class' : 'playlist-videos-container yt-scrollbar-dark yt-scrollbar'})
		for item in divs.find_all('li', attrs={'class' : 'yt-uix-scroller-scroll-unit'}):
			self.title_list[item['data-video-title']] = item['data-video-id']

#for downloading playlist from url
	def getPlaylist_videos_url(self,playlist_url):
		print('oh yeah')
		req = self.requestUrl(playlist_url)
		soup = BeautifulSoup(urlopen(req).read(),"html.parser")
		divs = soup.find('div', attrs={'class' : 'playlist-videos-container yt-scrollbar-dark yt-scrollbar'})
		for item in divs.find_all('li', attrs={'class' : 'yt-uix-scroller-scroll-unit'}):
			self.title_list[item['data-video-title']] = item['data-video-id']

	def downloadallPlaylist(self,quality):
		if quality != 'default':
			#dosomething
			for keys in self.title_list:
				q = self.findQuality(self.title_list[keys])
				self.crawlQualitylink(quality_choice)
		else:
			for keys in self.title_list:
				q = self.findQuality(self.title_list[keys])
				self.crawlQualitylink(quality)
		
	def selectPlaylist_videos(self,quality):
		videos_playlist=list(self.title_list.keys())
		videos_playlist = '""" FALSE """'.join(videos_playlist)
		playlist_choice=subprocess.getstatusoutput('zenity --title="""video""" --list --checklist --column """ """ --column """Playlist list""" FALSE """'+videos_playlist+'"""')[1].split("\n")[1].split("|")
		print(playlist_choice)
		if quality != 'default':
			for title in playlist_choice:
				q = self.findQuality(self.title_list[title])
				self.crawlQualitylink(quality)
		else:
			for title in playlist_choice:
				q = self.findQuality(self.title_list[title])
				self.crawlQualitylink(quality)

	# def qualitySettings(self,playlist_choice):
	# 	choice = self.selectLink(playlist_choice)

	def selectLink(self):
		choice = self.title_list[next(iter(self.title_list))]
		quality = self.findQuality(choice)
		return(quality)


