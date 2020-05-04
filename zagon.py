#!/usr/bin/python3

from guizero import *
import subprocess
from time import sleep


#import os
#print(os.listdir('.'))

def cubicSDR():
	cmd = ['CubicSDR']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def fmRadio():
	cmd = ['/home/pi/MMAnalizator/FMsprejemnikRDS.py']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def dab():
	cmd = ['/home/pi/MMAnalizator/qt-dab/linux-bin/qt-dab']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def dvbtSignal():
	cmd = ['lxterminal', '-e', 'dvb-fe-tool', '--femon']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

def dvbtScan():
	cmd = ['lxterminal', '-e', 'w_scan']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

# dvbv5-scan si-Channel -F -o dvb_scan_out.conf -v
def dvbtSeznam():
	cmd = ['lxterminal', '-e', 'dvbv5-scan', '/home/pi/si-Channel', '-v','-F', '--output=dvb_scan_out.conf']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

def dvbPosnemiTS():
	#cmd = ['lxterminal', '-e','/home/pi/MMAnalizator/posnemiTS.sh']
	cmd = ['lxterminal -e python3 /home/pi/MMAnalizator/posnemi.py']
	#cmd = ['python3 /home/pi/MMAnalizator/posnemi.py']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
	#proces = subprocess.Popen(cmd, creationflags=CREATE_NEW_CONSOLE)
	
	if proces == 0:
		erorr_text.clear()
		erorr_text.append("Transport Stream uspešno zapisan v datoteko  [ " + preberiDatoteko("/tmp/dvbTmpImeTS") +" ]\n\nSedaj lahko analiziraš TS\ns pomočjo DVBinspectorja ali pa si ogledaš\nposnet TS v programu VLC.")
	else:
		erorr_text.clear()
		erorr_text.append("Napaka pri izvajanju TS snemanja.")
	app.display()

def dvbtInspector():
	cmd = ['lxterminal', '-e','/home/pi/MMAnalizator/DVBinspector/dvb.sh']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

def vlcTS():
	cmd = ['vlc', '-vvv', preberiDatoteko("/tmp/dvbTmpImeTS")]
	proces = subprocess.call(cmd)
	app.display()


def preberiDatoteko(datoteka):
	f = open(datoteka, "r")
	return f.read().rstrip()

app = App(title="Zagon analizatorjev", layout="auto", height=1000, width=1000)
welcome_message = Text(app, text="Izberi kaj želiš analizirati:", width="fill", height=3, size=15)

sirina = 20
visina = 2
text_error = ""

PushButton(app, width=sirina, height=visina, command=cubicSDR, text="CubicSDR" )
PushButton(app, width=sirina, height=visina, command=fmRadio, text="FM radio" )
PushButton(app, width=sirina, height=visina, command=dab, text="DAB+" )

PushButton(app, width=sirina, height=visina, command=dvbtScan, text="DVB-T Scan" )
PushButton(app, width=sirina, height=visina, command=dvbtSeznam, text="DVB-T pridobi programski seznam" )

PushButton(app, width=sirina, height=visina, command=dvbPosnemiTS, text="Posnemi TS stream" )
PushButton(app, width=sirina, height=visina, command=dvbtInspector, text="DVBinspector" )
PushButton(app, width=sirina, height=visina, command=vlcTS, text="VLC (odpre posnet TS)" )

erorr_text = Text(app, text=text_error, width="fill", height=5, size=12)

app.display()
