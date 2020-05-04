#!/usr/bin/python3

# Imports
import os, sys, subprocess, threading, time, signal, fcntl

class TestThreading(object):
	def __init__(self, interval=1):
		self.interval = interval
		self.thread = threading.Thread(target=self.run, args=())
		self.thread.daemon = True
		self.dela = True
	
	def startSnoop(self):
		self.thread.start()
		self.dela = True
		
	def run(self):
		cmdRecord = "dvbsnoop -s ts -tsraw -b >" +celotnaPot
		recordProc = subprocess.Popen("exec " + cmdRecord, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		
		startCas = time.time()
		endCas = startCas + casSnemanja
		
		self.vrniNapako = 0
		
		fd = recordProc.stdout.fileno()
		fl = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
		
		while time.time() < endCas:
			time.sleep(1)
			print("Preostali cas snemanja: "+str(int(casSnemanja)-int(round(time.time()-startCas)))+" s")
			
			
			izpisSnoop = recordProc.stdout.readline().decode("utf-8") 
			#dodaj preverjanje erorjev
			if(izpisSnoop):
				print(">> "+izpisSnoop)
				if "Permission denied" in izpisSnoop:
					self.vrniNapako = 1 # napaka pri pisanju najbrz
					break
			
			'''
			if(err):
				print(err)
				self.vrniNapako = 2 # error programa
				break
			'''
			
		#recordProc.terminate()
		recordProc.terminate()
		print (recordProc.pid)
		print ("Proc snemanje killed")
		self.dela = False
	
	def izhodPodatki(self):
		if not self.dela:
			return self.vrniNapako # vrne kodo napake ali 0 ce je koncalo
		else:
			return -1 # se snema

crta = "\n----------------------------------------------\n"

casSnemanja = 5 #sekunde
casSnemanja = input("Vnesi koliko sekund zelis snemati TS [privzeto: "+str(casSnemanja)+"]: ") or casSnemanja
casSnemanja = int(casSnemanja)

vhodnaDatoteka = "/home/pi/MMAnalizator/dvb_scan_out.conf"
vhodnaDatoteka = input("Vnesi datoteko za izbiro multipleksa [privzeto: "+vhodnaDatoteka+"]: ") or vhodnaDatoteka

multipleks = 'KOPER'
multipleks = input("Vnesi enega izmed programov v multipleksu, ki bi ga rad posnel [privzeto: "+multipleks+"]: ") or multipleks

imeIzhodne = "posnetPY.ts"
potIzhodne = "/home/pi/MMAnalizator/posnemi/"

imeIzhodne = input("Vnesi ime izhodne datoteke [privzeto: "+imeIzhodne+"]: ") or imeIzhodne

celotnaPot = potIzhodne+imeIzhodne

#TODO PREVERI USER INPUTE


def tuneFunction():
	print(crta+'Zaganjam DVB-T sprejemnik'+crta)
	cmdTune = ['dvbv5-zap', '-c', vhodnaDatoteka, '-I', 'DVBV5', multipleks, '-r']
	tuneProc = subprocess.Popen(cmdTune, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	tr = TestThreading()
	
	for line in iter(tuneProc.stdout.readline, b''):
		
		# izpis samo ce je tekst v vrstici (ker dvbv5 pise prazne vrstice vmes
		if line.strip():
			print("> "+ line.rstrip().decode("utf-8"))
		
		# beri izhod in ce detektas dolocene stringe naredi nekej
		if 'DVR interface ' in line.rstrip().decode("utf-8") :
			# Write something to stdout
			print(crta+'Zaganjam TS rekorder\nSnemanje v datoteko '+celotnaPot+crta)
			
			tr.startSnoop()
		
		if tr:
			rezultatSnemanja = tr.izhodPodatki()
			if rezultatSnemanja != -1: #ce je rezultatsnemanja razlicen od -1 se je dvbsnoop ustavil, zakaj izves iz return kode
				tuneProc.kill()
				tuneProc.terminate()
				print (tuneProc.pid)
				print ("Proc tune killed")
	return rezultatSnemanja

rezultat = tuneFunction()

if rezultat == 0:
	print(crta+"TS je bil uspesno posnet v datoteko "+celotnaPot+crta)
	#zapisi pot do posnete datoteke v /tmp/dvbTmpImeTS
	f = open("/tmp/dvbTmpImeTS", "w")
	f.write(celotnaPot)
	f.close()
elif rezultat == 1:
	print(crta+"Pri snemanju TS je prislo do napake!"+crta)
	input("Press Enter to continue...")
elif rezultat == 2:
	print(crta+"Pri snemanju TS je prislo do napake!"+crta)
	input("Press Enter to continue...")
