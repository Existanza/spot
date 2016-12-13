import requests
from bs4 import BeautifulSoup
import time
import io
import subprocess as sp
import re
import os
from sys import platform
import spotilib


def got_lyrics():
	if os.path.exists('lyrics.txt') and os.stat('lyrics.txt').st_size > 30:
		return True
	else:
		return False


def from_plyrics(artist, song):
	artist = re.sub('[^a-z]+', '', artist)
	song = re.sub('[^a-z]+', '', song)
	url = 'http://www.plyrics.com/lyrics/' + artist + '/' + song + '.html'
	print("Fetching the lyrics from " + url)
	r = requests.get(url)
	r.encoding = 'utf-8'
	rt = r.text
	lyrics = rt[rt.find('<!-- start of lyrics -->'):rt.find('<!-- end of lyrics -->')][26:]
	soup = BeautifulSoup(lyrics, "lxml")
	text = soup.get_text()
	with io.open('lyrics.txt', 'w', encoding='utf-8') as f:
		f.write(text)


def from_tekstowo(artist, song):
	artist = artist.replace(" ", "_")
	artist = re.sub('[^a-z_]+', '', artist)
	song = song.replace(" ", "_")
	song = re.sub('[^a-z_]+', '', song)
	url = 'http://www.tekstowo.pl/piosenka,' + artist + ',' + song + '.html'
	print("Fetching the lyrics from " + url)
	r = requests.get(url)
	r.encoding = 'utf-8'
	rt = r.text
	lyrics = rt[rt.find('Tekst piosenki:'):rt.find('Poznaj histori')][50:]
	soup = BeautifulSoup(lyrics, "lxml")
	text = soup.get_text()
	with io.open('lyrics.txt', 'w', encoding='utf-8') as f:
		f.write(text)


def get_new_lyrics(artist, song, proc):
	from_plyrics(artist, song)
	if not got_lyrics():
		from_tekstowo(artist, song)
		if not got_lyrics():
			if os.path.exists('lyrics.txt'):
				os.remove('lyrics.txt')
			print("Lyrics unavailable")
	if proc is not None:
		proc.kill()
	if os.path.exists('lyrics.txt'):
		print("Fetched successfully")
		if platform.startswith('linux'):
			proc = sp.Popen(["gedit", "lyrics.txt"])
		elif platform.startswith('win'):
			proc = sp.Popen(["notepad.exe", "lyrics.txt"])
	return artist, song, proc

ac, sc = ('',)*2
pc = None
if os.path.exists('lyrics.txt'):
	os.remove('lyrics.txt')

while True:
	a = spotilib.artist().lower()
	a = a.replace("é", "e")
	if a[:3] == "the":
		a = a[3:]
	s = spotilib.song().lower()
	if a != ac or s != sc:
		print(spotilib.song_info())
		ac, sc, pc = get_new_lyrics(a, s, pc)
		print()
	time.sleep(1)
