#!/usr/bin/python3
from crawlurl import *

def formatquery():
	query=subprocess.getstatusoutput('zenity --entry --title="Query Box" --text="Enter your query" --entry-text "Query"')[1].split("\n")[1]
	query=query.strip().split()
	query="+".join(query)
	htmlurl = "https://www.youtube.com/results?search_query="+ query
	return(htmlurl)

def geturl():
	Utubeurl=subprocess.getstatusoutput('zenity --entry --title="URL Box" --text="Enter URL" --entry-text "Youtube Url"')[1].split("\n")[1]	
	return(Utubeurl)

def getPlaylistdownload():
	download_type = subprocess.getstatusoutput('zenity --title="vidoe download type" --list  --column "download type" "Download all" "choose some" "settings"')[1].split("\n")[1]
	return(download_type)



download_type = subprocess.getstatusoutput('zenity --title="vidoe quality" --list  --column "download type" "stand alone link" "playlist" "from url"')[1].split("\n")[1]
if download_type == 'stand alone link':
	t = 1
	htmlurl = formatquery()
	c = crawlUrl(t,htmlurl)
	dict_standalone = c.crawlQuery()
	videos_standalone=list(dict_standalone.keys())
	videos_standalone = '""" FALSE """'.join(videos_standalone)
	videos_choice=subprocess.getstatusoutput('zenity --title="""video""" --list --radiolist --column """ """ --column """video list""" FALSE """'+videos_standalone+'"""')[1].split("\n")[1]
	downloads = c.selectLink(videos_choice)
	quality=list(downloads.keys())
	quality = "' FALSE '".join(quality)	
	quality_choice=subprocess.getstatusoutput("zenity --title='video quality' --list --radiolist --column '' --column 'video quality' FALSE 'default' FALSE '"+quality+"'")[1].split("\n")[1]
	c.crawlQualitylink(quality_choice)


elif download_type == 'playlist':
	t = 2
	htmlurl = formatquery()
	c = crawlUrl(t,htmlurl)
	dict_playlist = c.crawlQuery()
	videos_playlist=list(dict_playlist.keys())
	videos_playlist = '""" FALSE """'.join(videos_playlist)
	playlist_choice=subprocess.getstatusoutput('zenity --title="""video""" --list --radiolist --column """ """ --column """Playlist list""" FALSE """'+videos_playlist+'"""')[1].split("\n")[1]
	c.getPlaylist_videos(playlist_choice)
	download_type = getPlaylistdownload()

	quality_choice = 'default'
	
	while download_type == 'settings':
		quality_setting = subprocess.getstatusoutput('zenity --title="video download type" --list  --column "quality settings" "default" "manual"')[1].split("\n")[1]
		if quality_setting != 'default':
			#Do something
			downloads = c.selectLink()
			quality=list(downloads.keys())
			quality = "' FALSE '".join(quality)	
			quality_choice=subprocess.getstatusoutput("zenity --title='video quality' --list --radiolist --column '' --column 'video quality' FALSE 'default' FALSE '"+quality+"'")[1].split("\n")[1]
		else:
			quality_choice = quality_setting
		download_type = getPlaylistdownload()
	
	if download_type == "Download all":
		c.downloadallPlaylist(quality_choice)
	elif download_type == 'choose some':
		c.selectPlaylist_videos(quality_choice)

else:
	t = 3
	htmlurl = geturl()
	if '&list' in htmlurl :
		c = crawlUrl(t,htmlurl)
		c.getPlaylist_videos_url(htmlurl)
		download_type = getPlaylistdownload()

		quality_choice = 'default'
		
		while download_type == 'settings':
			quality_setting = subprocess.getstatusoutput('zenity --title="video download type" --list  --column "quality settings" "default" "manual"')[1].split("\n")[1]
			if quality_setting != 'default':
				#Do something
				downloads = c.selectLink()
				quality=list(downloads.keys())
				quality = "' FALSE '".join(quality)	
				quality_choice=subprocess.getstatusoutput("zenity --title='video quality' --list --radiolist --column '' --column 'video quality' FALSE 'default' FALSE '"+quality+"'")[1].split("\n")[1]
			else:
				quality_choice = quality_setting
			download_type = getPlaylistdownload()
		
		if download_type == "Download all":
			c.downloadallPlaylist(quality_choice)
		elif download_type == 'choose some':
			c.selectPlaylist_videos(quality_choice)
	else:
		c = crawlUrl(t,htmlurl)
		downloads = c.findQuality(htmlurl)
		quality=list(downloads.keys())
		quality = "' FALSE '".join(quality)	
		quality_choice=subprocess.getstatusoutput("zenity --title='video quality' --list --radiolist --column '' --column 'video quality' FALSE 'default' FALSE '"+quality+"'")[1].split("\n")[1]
		c.crawlQualitylink(quality_choice)
		print("DONE")