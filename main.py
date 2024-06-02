from manim import *
from furigana import *
import syncedlyrics

from datetime import datetime

imports=r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{CJKutf8}
\newcommand{\jap}[1]{\text{\begin{CJK}{UTF8}{min}#1\end{CJK}}}
"""

template = TexTemplate(preamble=imports)

class Lyrics(Scene):
	def construct (self):
		print("Enter image link: ", end="")
		img = input()
		
		print("Enter song name: ", end="")
		name = input()
		
		print("Enter song runtime in seconds: ", end="")
		time_end = float(input())
		
		image = ImageMobject(img, scale_to_resolution=1080)
		self.add(image)
		
		lrc = syncedlyrics.search(name)
		
		timestamp = []
		lyrics = []
		
		for line in lrc.split("\n"):
			if (line==""): continue
			
			line = line.split(" ",1)
			if (len(line)==1 or line[1]==""): continue
			(time, text) = line
			t = datetime.strptime(time[1:-1],"%M:%S.%f").time()
			
			timestamp.append(t.minute * 60 + t.second + t.microsecond/1000000)
			res = ""
			print(text,split_furigana(text))
			for x in split_furigana(text):
				if (len(x)==1): res+=r"\stackrel{}{\jap{"+x[0]+"}}"
				else: res+=r"\stackrel{\jap{"+x[1]+r"}}{\jap{"+x[0]+"}}"\
			
			lyrics.append(res)
		
		lyrics += ["",""]
		timestamp += [time_end]
		
		if (timestamp[0]!=0):
			lyrics = [""]+lyrics
			timestamp = [0]+timestamp
		
		#print(lyrics)
		#print(timestamp)
		
		for i in range(len(lyrics)):
			lyrics[i] = MathTex(lyrics[i],tex_template = template)
			lyrics[i].set_background_stroke(color=BLACK, width=5)
			if (i%2==0): lyrics[i] = lyrics[i].shift(UP)
			else: lyrics[i] = lyrics[i].shift(DOWN)
		
		self.add(lyrics[0])
		self.add(lyrics[1])
		
		for i in range(1,len(timestamp)):
			self.wait(timestamp[i]-timestamp[i-1])
			self.remove(lyrics[i-1])
			self.add(lyrics[i+1])
			lyrics[i].set_color(BLUE)
		
