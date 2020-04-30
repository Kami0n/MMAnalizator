#!/bin/bash
# setup.sh

######################## celoten setup za MMAnalizator ########################

## ##################### FUNKCIJE #####################
get_latest_release() {
	curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
	grep '"tag_name":' |                                            # Get tag line
	sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}

## ##################### SETUP #####################

sudo apt-get update -y

sudo apt install -y unzip
sudo apt install -y cubicsdr
sudo apt install -y gnuradio gr-osmosdr gr-rds
sudo apt install -y dvb-tools dvbsnoop w-scan

#chmod +x *.sh
#chmod +x *.py

#dodaj LL
#echo "alias ll='ls -laF'" >> /home/pi/.bashrc
#sed -i "/^#.* alias ll='ls -l' /s/^#//" /home/pi/.bashrc
grep -qxF "alias ll='ls -laF'" /home/pi/.bashrc || echo "alias ll='ls -laF'" >> /home/pi/.bashrc

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
#./script-for-debian

# --------------------- DVBinspector ---------------------
wget "http://www.digitalekabeltelevisie.nl/dvb_inspector/img/DVBinspector-1.12.0-dist.zip"
unzip -q DVBinspector-1.12.0-dist.zip


# dodaj zagon v startup
#vsebina="[Desktop Entry]
#Type=Application
#Name=zagon
#Exec=/usr/bin/python3 /home/pi/zagon/zagon.py"
#mkdir -p /home/pi/.config/autostart/
#echo "$vsebina" > /home/pi/.config/autostart/zagon.desktop



read -p "Za izhod kilkni katerikoli gumb." x

#sudo reboot
exit 0
