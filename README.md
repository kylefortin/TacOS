# TacOS
Fully customizable auxiliary lighting and accessory relay control interface.
Built on the PyQt5 UI framework.
Designed to interface from a Raspberry Pi via the I2C bus to an external 12V relay shield.
Optional interface to external composite video device via composite video to USB adapter.

## Current Version

Current version is `2.2.0`

## Dependencies
  +*TacOS requires SIP, PyQt5 and QScintilla to be built and installed on the local machine.*  
  +*TacOS setup scripts assume that the TacOS directory is located within `/home/pi`.*

## Installation
### Building Dependent Frameworks
#### Installing QT5 Core Tools
1. Install QT5 Core Tools from APT `sudo apt-get install qt5-default`
#### Building/Installing SIP
1. Start from a fresh install of Raspbian Stretch.
2. Download SIP from https://www.riverbankcomputing.com/software/sip/download.
3. Open a new terminal shell.
4. Navigate to the folder that you just downloaded the files to.
5. Extract the SIP tar.gz file `tar -xzvf <sip>.tar.gz`.
6. Navigate to the new SIP directory `cd /<sip>`.
7. Configure SIP for build `python3 configure.py --sip-module=PyQt5.sip`.
8. Create makefile for installation `make`.
9. Install makefile using `sudo make install`.
#### Building/Installing PyQt5
1. Download PyQt5 from https://www.riverbankcomputing.com/software/pyqt/download5.
2. Extract the PyQt5 tar.gz file `tar -xzvf <pyqt5>.tar.gz`.
3. Navigate to the new PyQt5 directory `cd /<pyqt5>`.
4. Configure PyQt5 for build using `python3 configure.py`.
5. Create makefile for installation `make`.
6. Install makefile `sudo make install`.
#### Building/Installing QScintilla
1. Download QScintilla from https://www.riverbankcomputing.com/software/qscintilla/download.
2. Extract the QScintilla tar.gz file using `tar -xzvf <qscintilla>.tar.gz`.
3. Navigate to the Qt4Qt5 subdirectory using `cd /<qscintilla>/Qt4Qt5`.
4. Build the qmake file `qmake`.
5. Build the makefile `make`.
6. Install the makefile `sudo make install`.
7. Navigate to the Python subdirectory `cd /<qscintilla>/Python`.
8. Configure the Python binding for build using `python3 configure.py --pyqt=PyQt5`.
9. Build the makefile using `make`.
10. Install the makefile using `sudo make install`.
### Installing Dependent Packages
1. Navigate to the TacOS directory `cd /home/pi/TacOS`.
2. Install the requirements `pip3 install -r requirements.txt`.
### Installing ATLAS
1. Install the ATLAS package from APT `sudo apt-get install libatlas-base-dev`
### Configure Pi for Automatic Startup to TacOS
1. Navigate to the TacOS directory `cd /home/pi/TacOS`.
2. Run the Pi setup script `sh setup-rpi.sh`.
3. When prompted with the RasPi Config interface, make sure to enable SSH and the I2C interface.