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
	print("DONE")
elif download_type == 'playlist':
	t = 2
	htmlurl = formatquery()
else:
	t = 3
	htmlurl = geturl()
	c = crawlUrl(t,htmlurl)
	downloads = c.findQuality(htmlurl)
	quality=list(downloads.keys())
	quality = "' FALSE '".join(quality)	
	quality_choice=subprocess.getstatusoutput("zenity --title='video quality' --list --radiolist --column '' --column 'video quality' FALSE 'default' FALSE '"+quality+"'")[1].split("\n")[1]
	c.crawlQualitylink(quality_choice)