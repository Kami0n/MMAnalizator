#!/bin/bash
# setup.sh

######################## celoten setup za MMAnalizator ########################

## ##################### FUNKCIJE #####################
get_latest_release() {
	curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
	grep '"tag_name":' |                                            # Get tag line
	sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}

mojecho() {
	echo " "
	echo "----------------------------------------------------"
	echo $1
	echo $2
	echo "----------------------------------------------------"
	echo " "
}

## ##################### SETUP #####################

mojecho " Zacetek zacetnih nastavitev."

#dodaj LL
#echo "alias ll='ls -laF'" >> /home/pi/.bashrc
#sed -i "/^#.* alias ll='ls -l' /s/^#//" /home/pi/.bashrc
grep -qxF "alias ll='ls -laF'" /home/pi/.bashrc || echo "alias ll='ls -laF'" >> /home/pi/.bashrc

chmod +x *.sh
chmod +x *.py

mojecho " Zakljucek zacetnih nastavitev." " Zacetek instalacije komponent z apt install."

sudo apt-get update -y

sudo apt install -y unzip
sudo apt install -y cubicsdr
sudo apt install -y gnuradio gr-osmosdr gr-rds
sudo apt install -y dvb-tools dvbsnoop w-scan
pip3 install guizero

mojecho " Zakljucena instalacija komponent z apt install." " Instaliram Qt-DAB"

# --------------------- Qt-DAB ---------------------
verzijaDAB=$(get_latest_release "JvanKatwijk/qt-dab")
echo "Zadnja verzija Qt-DAB: $verzijaDAB"
wget "https://github.com/JvanKatwijk/qt-dab/archive/$verzijaDAB.tar.gz"
tar -xf "$verzijaDAB.tar.gz"
cd "qt-dab-$verzijaDAB"
sed -i '/+= sdrplay-v2/ s/^#*/#/' qt-dab.pro
sed -i '/+= sdrplay-v3/ s/^#*/#/' qt-dab.pro
sed -i '/+= lime/ s/^#*/#/' qt-dab.pro
sed -i '/+= airspy/ s/^#*/#/' qt-dab.pro
sed -i '/+= hackrf/ s/^#*/#/' qt-dab.pro
sed -i '/+= soapy/ s/^#*/#/' qt-dab.pro
./script-for-debian

mojecho " Zakljucena instalacija Qt-DAB." " Instaliram DVBinspector."

# --------------------- DVBinspector ---------------------
cd ..
wget "http://www.digitalekabeltelevisie.nl/dvb_inspector/img/DVBinspector-1.12.0-dist.zip"
unzip -q DVBinspector-1.12.0-dist.zip

mojecho " Zakljucena instalacija DVBinspector." " Dodajam skripto zagon.py v startup."

# dodaj zagon v startup
vsebina="[Desktop Entry]
Type=Application
Name=zagon
Exec=/usr/bin/python3 /home/pi/MMAnalizator/zagon.py"
mkdir -p /home/pi/.config/autostart/
echo "$vsebina" > /home/pi/.config/autostart/zagon.desktop

mojecho " Programi so pripravljeni na uporabo." " Raspberry Pi se mora sedaj na novo zagnati!"
read -p "Za ponovni zagon kilkni katerikoli gumb. (Za izhod pa Ctrl+C)" x
sudo reboot
#exit 0
