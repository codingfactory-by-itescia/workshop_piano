# Montage

Voici le montage pour une LED

![Montage](images/1led.png)

# Installation

## Installation du système de la Raspberry PI
Télécharger [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)\
Choisissez l'OS `Raspberry Pi OS (other) > Raspberry Pi OS Lite` ainsi que votre micro SD puis cliquez sur **Write**\
Ouvrez votre console de commande puis naviguez à l'emplacement du système de votre Raspberry Pi:
- Sur Mac OS: `/Volumes/boot`

### Setup du SSH

Exécutez la commandes à la racine du système de votre Raspberry Pi:
```sh
# Sur Powershell
echo $null >> ssh 

# Sur Mac / Linux
touch ssh
```

### Setup du Wifi

Créez un fichier wpa_supplicant.conf à la racine du système de votre Raspberry Pi à la racine du système de votre Raspberry Pi:
```sh
touch wpa_supplicant.conf
```
avec le contenu
```conf
country=FR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    scan_ssid=1
    ssid="your_wifi_ssid"
    psk="your_wifi_password"
}
```

# Setup du clavier MIDI

## Configuration de base

Ajoutez la ligne suivante au fichier `/boot/config.txt`
```
audio_pwm_mode=2
```

Vous pouvez désormais mettre votre carte micro SD dans votre Raspberry Pi puis vous connecter en SSH à cette dernière.

Installer les paquets suivants:
```sh
sudo apt-get install fluidsynth alsa-utils screen -y
```

Puis lancez le synthétiseur:
```sh
screen # Pour ouvrir un nouveau terminal virtuel

# Lancez cette commande dans le screen
fluidsynth --audio-driver=alsa --gain 5 /usr/share/sounds/sf2/FluidR3_GM.sf2

# Pour vous détacher de cette session virtuelle, utilisez le raccourcis clavier "ctrl+a d"
```

## Configurer la sortie son de la Raspberry PI

Brancher le clavier MIDI en USB sur la Rapsberry PI\
Brancher l'enceinte en jack sur la Raspberry PI\
Lancer la commande `aconnect -o`\
Cette commande devrait vous donner ce type d'output:
```sh
client 14: 'Midi Through' [type=kernel]
    0 'Midi Through Port-0'
client 20: 'VMini' [type=kernel,card=1]
    0 'VMini MIDI 1    '
    1 'VMini MIDI 2    '
client 128: 'FLUID Synth (1037)' [type=user,pid=1037]
    0 'Synth input port (1037:0)'
```
Dans notre cas, nous voulons connecter notre clavier MIDI à la sortie audio de Fluid Synth, la commande à lancer sera donc:
```sh
aconnect 20:0 128:0
```

## Installation du projet
Installation de Python 3 et de pip3:
```sh
sudo apt-get update
sudo apt-get install git python3 idle3 python3-pip

# Pour utiliser python3 par défaut
sudo update-alternatives --install /usr/bin/python python $(which python3) 2
```

Dépendences: 

```sh
sudo apt-get update
sudo apt-get install python-smbus

pip3 install \
    rtmidi \ # Sert à récupérer l'appui des touches du clavier midi
    adafruit-circuitpython-mcp230xx \ # Wrapper pour intéragir avec le MCP23017
    adafruit-blinka # Pour avoir accès aux librairies board et busio
```

Activation du bus I2C:
```sh
sudo raspi-config
# Puis naviguez dans le menu "5 Interfacing Options">"I2C" et sélectionnez "Yes"

# Redémarez la Raspberry
sudo reboot
```

Clonage du projet:
```sh
git clone https://github.com/codingfactory-by-itescia/workshop_piano.git

cd workshop_piano/piano_controller

sudo chmod +x ./main.py

### Note
### Si vous voulez que le programme ne puisse s'exécuter qu'une seule fois, modifiez la constante DEBUG en lui mettant la valeur True
./main.py 
```

# Références

[Installation et paramétrage de Raspberry Pi OS](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html)

[Paramétrage de la sortie son](https://medium.com/@rreinold/how-to-use-a-raspberry-pi-3-to-turn-midi-piano-to-into-stand-alone-powered-piano-4aeb79e309ce)

