#!/usr/bin/python3

from guizero import *
from time import sleep
import re, subprocess, os 

dir_path = os.path.dirname(os.path.realpath(__file__))
print ("Trenutni direktorij: " + dir_path)


def cubicSDR():
	cmd = ['CubicSDR']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def fmRadio():
	cmd = [dir_path+'/FMsprejemnikRDS.py']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def dab():
	cmd = [dir_path+'/qt-dab/linux-bin/qt-dab']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def dvbtSignal():
	cmd = ['lxterminal', '--working-directory='+dir_path+'/', '-e', 'dvb-fe-tool', '--femon']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

def dvbtScan():
	cmd = ['lxterminal', '--working-directory='+dir_path+'/', '-e', 'w_scan', '-ft', '-cSI']  #, '>test.conf'
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

# dvbv5-scan si-Channel -F -o dvb_scan_out.conf -v
#cmd = ['lxterminal', '-e', 'dvbv5-scan', '/home/pi/MMAnalizator/si-Channel', '-v','-F', '--output=dvb_scan_out.conf']

# dvbv5-scan full-Spectrum -v -o dvb_scan_out.conf 
def dvbtSeznam():
	cmd = ['lxterminal', '--working-directory='+dir_path+'/', '-e', 'dvbv5-scan', 'full-Spectrum', '-v','--output=dvb_scan_out.conf']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	
	f = open(dir_path+"/dvb_scan_out.conf", "r")
	celotenFile = f.read()
	samoProgrami = re.findall('\[(.*?)\]',celotenFile);
	erorr_text.clear()
	erorr_text.append("Vsi DVB-T programi, ki so na voljo:\n")
	erorr_text.append('\n'.join(samoProgrami))
	app.display()

def dvbPosnemiTS():
	#cmd = ['lxterminal', '-e','/home/pi/MMAnalizator/posnemiTS.sh']
	cmd = ['lxterminal --working-directory='+dir_path+'/ -e  python3 posnemi.py']
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
	cmd = ['lxterminal', '-e',''+dir_path+'/DVBinspector/dvb.sh']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

def vlcTS():
	cmd = ['vlc', '-vvv', preberiDatoteko("/tmp/dvbTmpImeTS")]
	proces = subprocess.call(cmd)
	app.display()


def preberiDatoteko(datoteka):
	f = open(datoteka, "r")
	return f.read().rstrip()

app = App(title="Zagon analizatorjev", height=1000, width=1000, layout="grid")
welcome_message = Text(app, text="Izberi kaj želiš analizirati:", width="fill", height=3, size=15, grid=[0,0,2,1])

sirina = 20
visina = 2
text_error = ""

PushButton(app, width=sirina, height=visina, grid=[0,1], command=cubicSDR, text="CubicSDR")
PushButton(app, width=sirina, height=visina, grid=[0,2], command=fmRadio, text="FM radio" )
PushButton(app, width=sirina, height=visina, grid=[0,3], command=dab, text="DAB+" )

#PushButton(app, width=sirina, height=visina, command=dvbtScan, text="DVB-T Scan" )
PushButton(app, width=sirina, height=visina, grid=[0,4], command=dvbtSeznam, text="DVB-T full scan" )

PushButton(app, width=sirina, height=visina, grid=[0,5], command=dvbPosnemiTS, text="Posnemi TS stream" )
PushButton(app, width=sirina, height=visina, grid=[0,6], command=dvbtInspector, text="DVBinspector" )
PushButton(app, width=sirina, height=visina, grid=[0,7], command=vlcTS, text="VLC (odpre posnet TS)" )

erorr_text = Text(app, text=text_error, width=100, height=20, size=12, grid=[1,1,1,6] )

erorr_text.clear()
erorr_text.append(" ");

app.display()
