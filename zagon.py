#!/usr/bin/python3

from guizero import *
from time import sleep
import re, subprocess, os 

dir_path = os.path.dirname(os.path.realpath(__file__))
print ("Trenutni direktorij: " + dir_path)


def cubicSDR():
	cmd = ['CubicSDR']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def gqrxSDR():
	cmd = ['gqrx']
	subprocess.call(cmd, stdout=subprocess.PIPE)

def fmRadio():
	cmd = [dir_path+'/RPi4_FM_S_RDS.py']
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
	cmd = ['lxterminal --working-directory='+dir_path+'/ -e python3 posnemi.py']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
	
	if proces == 0:
		erorr_text.clear()
		erorr_text.append("Transport stream je bil uspešno zapisan v datoteko:\n[ " + preberiDatoteko("/tmp/dvbTmpImeTS") +" ]\n\nSedaj lahko analiziraš TS s pomočjo DVBinspectorja\nali pa si ogledaš posnet TS v programu VLC.")
	else:
		erorr_text.clear()
		erorr_text.append("Napaka pri izvajanju TS snemanja.")
	app.display()

def dvbtInspector():
	#cmd = ['lxterminal', '-e',''+dir_path+'/DVBinspector/dvb.sh']
	cmd = ['lxterminal', '-e','/home/pi/DVBinspector/dvb.sh']
	proces = subprocess.call(cmd, stdout=subprocess.PIPE)
	app.display()

def vlcTS():
	cmd = ['vlc', '-vvv', preberiDatoteko("/tmp/dvbTmpImeTS")]
	proces = subprocess.call(cmd)
	app.display()


def preberiDatoteko(datoteka):
	f = open(datoteka, "r")
	return f.read().rstrip()

app = App(title="Zagon analizatorjev", height=530, width=750, layout="grid")

paddingboxTop = Box(app, width="fill", align="top", grid=[0,0], height=10)
#paddingboxBottom = Box(app, width="fill", align="top", border=True, grid=[0,0], height=10)
paddingboxLeft = Box(app, width=10, align="top", grid=[0,1], height=10)
#paddingboxRight = Box(app, width="fill", align="top", border=True, grid=[0,0], height=10)

title_box = Box(app, width="fill", align="top", grid=[1,1])
welcome_message = Text(title_box, text="Izberi kaj želiš analizirati:")


button_box = Box(app, width="fill", align="left", grid=[1,2])
sirina = 20
visina = 2
PushButton(button_box, width=sirina, height=visina, command=cubicSDR, text="CubicSDR")
PushButton(button_box, width=sirina, height=visina, command=gqrxSDR, text="GQRX SDR")
PushButton(button_box, width=sirina, height=visina, command=fmRadio, text="FM radio" )
PushButton(button_box, width=sirina, height=visina, command=dab, text="DAB+" )
PushButton(button_box, width=sirina, height=visina, command=dvbtSeznam, text="DVB-T full scan" )
PushButton(button_box, width=sirina, height=visina, command=dvbPosnemiTS, text="Posnemi TS stream" )
PushButton(button_box, width=sirina, height=visina, command=dvbtInspector, text="DVBinspector" )
PushButton(button_box, width=sirina, height=visina, command=vlcTS, text="VLC (odpre posnet TS)" )

center_box = Box(app, width="fill", align="right", grid=[2,2])
erorr_text = Text(center_box, text="", width=60, height=20, size=12, grid=[1,1,1,6] )
erorr_text.clear()
erorr_text.append("V seznamu programov na levi strani okna izberi kaj želiš analizirati.");

app.display()
