#!/usr/bin/python3

# Imports
import os, sys, subprocess, threading, time, signal, fcntl, re

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
		#print (recordProc.pid)
		#print ("Proc snemanje killed")
		self.dela = False
	
	def izhodPodatki(self):
		if not self.dela:
			return self.vrniNapako # vrne kodo napake ali 0 ce je koncalo
		else:
			return -1 # se snema


dir_path = os.path.dirname(os.path.realpath(__file__))
print ("Trenutni direktorij: " + dir_path)
crta = "\n----------------------------------------------\n"

casSnemanjaDefault = "5" #sekunde
casSnemanja = input("Vnesi koliko sekund želiš snemati TS [privzeto: "+str(casSnemanjaDefault)+"]: ") or casSnemanjaDefault
while((not casSnemanja.isdigit()) or int(casSnemanja) <= 0):
	print("NAPAKA pri vnosu! Vnesel si [ "+casSnemanja+" ] ki ni pozitivno celo število!")
	casSnemanja = input("Vnesi koliko sekund želiš snemati TS [privzeto: "+str(casSnemanjaDefault)+"]: ") or casSnemanjaDefault
casSnemanja = int(casSnemanja)


vhodnaDatotekaDefault = "/home/pi/MMAnalizator/dvb_scan_out.conf"
vhodnaDatoteka = input("Vnesi datoteko za izbiro multipleksa [privzeto: "+vhodnaDatotekaDefault+"]: ") or vhodnaDatotekaDefault

f = open(vhodnaDatoteka, "r")
celotenFile = f.read()
samoProgrami = re.findall('\[(.*?)\]',celotenFile);

multipleksDefault = 'KOPER'
multipleks = input("Vnesi enega izmed programov v multipleksu, ki bi ga rad posnel [privzeto: "+multipleksDefault+"]: ") or multipleksDefault
while(multipleks not in samoProgrami):
	print("NAPAKA pri vnosu! Vnesel si program [ "+multipleks+" ] ki ne obstaja v seznamu programov")
	multipleks = input("Vnesi enega izmed programov v multipleksu, ki bi ga rad posnel [privzeto: "+multipleksDefault+"]: ") or multipleksDefault


imeIzhodneDefault = "posnetPY.ts"
potIzhodne = dir_path+"/"

imeIzhodne = input("Vnesi ime izhodne datoteke [privzeto: "+imeIzhodneDefault+"]: ") or imeIzhodneDefault

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
				#print (tuneProc.pid)
				#print ("Proc tune killed")
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
