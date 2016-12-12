import requests
from bs4 import BeautifulSoup
import time
import io
import subprocess as sp
import re
import spotilib

def run(artist, song, proc):
	if True:
		url = 'http://www.plyrics.com/lyrics/' + artist + '/' + song + '.html'
		print(url)
		rt = requests.get(url).text
		lyrics = rt[rt.find('<!-- start of lyrics -->'):rt.find('<!-- end of lyrics -->')][26:]
		soup = BeautifulSoup(lyrics, "lxml")
		text = soup.get_text()
		with io.open('out.txt','w',encoding='utf8') as f:
			f.write(text)
		if proc is not None:
			proc.kill()
		proc = sp.Popen(["notepad.exe", "out.txt"])
	return artist, song, proc

ac = ''
sc = ''
proc = None

while True:
	a = spotilib.artist().replace(" ", "").lower()
	re.sub('[^a-z]+$', '', a)
	if a[:3] == "the":
		a = a[3:]
	if a[:5] == "touch" and a[6:10] == "amor":
		a = "toucheamore"
	s = spotilib.song().replace(" ", "").lower()
	re.sub('[^a-z]+$', '', s)
	if a != ac or s != sc:
		ac, sc, proc = run(a, s, proc)
	time.sleep(1)
