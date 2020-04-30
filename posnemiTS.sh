#!/bin/bash
# posnemiTS.sh

cd /home/pi/

DIR=$PWD

read -p "Vnesi koliko sekund zelis snemati TS [privzeto: 10]: " CAS
CAS=${CAS:-10}

read -p "Vnesi datoteko za izbiro multipleksa [privzeto: /home/pi/dvb_scan_out.conf]: " DATOTEKA
DATOTEKA=${DATOTEKA:-/home/pi/dvb_scan_out.conf}

read -p "Vnesi kateri multipleks bi rad posnel (možnosti A ali C) [privzeto: A]: " MUX
MUX=${MUX:-A}

if [[ $MUX == A ]]
then
	PROGRAM="KOPER" # ne bo delalo v LJ
elif [[ $MUX == C ]]
then
	PROGRAM="SLO1"
else
	read -p "Napaka pri izbiri multipleksa! Za izhod kilkni en gumb." x
	exit 1
fi

read -p "Vnesi ime izhodne datoteke [privzeto: posnet.ts]: " IZHOD
IZHOD=${IZHOD:-posnet.ts}

echo " "
echo "----------------------------------------------------"
echo "TS se bo snemal ${CAS} sekund."
echo "Za izbiro multipleksa porabljam datoteko ${DATOTEKA}"
echo "Snemam program ${PROGRAM} iz multipleksa ${MUX}"
echo "----------------------------------------------------"
echo " "

timeout $((CAS + 5)) dvbv5-zap -c ${DATOTEKA} -I DVBV5 ${PROGRAM} -r &
PID1=$!
sleep 3

echo " "
echo "----------------------------------------------------"
echo "Začetek zapisovanja TS v datoteko ${DIR}/${IZHOD}"
echo "----------------------------------------------------"
echo " "
echo " "


timeout $((CAS)) dvbsnoop -s ts -tsraw -b > /home/pi/MMAnalizator/${IZHOD} 
PID2=$!
testvar=$PID2
echo $PID2
if [[ $testvar == *"Permission denied"* ]]; then
	IzhodNOTOK=$'NI OK'
	notOK=$true
fi


wait $PID1 $PID2


IzhodOK=$' \n---------------------------------------------------- \nTS posnet v datoteko ${DIR}/${IZHOD} \nSedaj lahko analiziraš TS s pomočjo DVBinspectorja ali pa si ogledaš posnet TS s pomočjo VLC. \n---------------------------------------------------- \n'


if [[ $notOK ]]; then
	echo "$IzhodNOTOK"
else
	echo "$IzhodOK"
fi


> /tmp/dvbTmpImeTS
echo "${DIR}/${IZHOD}" >> /tmp/dvbTmpImeTS


#read -p "Za izhod kilkni en gumb." x

exit 0