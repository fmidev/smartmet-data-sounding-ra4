# SmartMet Data Ingestion Module for TEMP (FM-35) data

Download and convert WMO TEMP (FM-35) observations for SmartMet Workstation and SmartMet Server.

DO NOT INSTALL THIS IF GTS MESSAGE SWITCH IS AVAILABLE LOCALLY. USE smartmet-data-sounding

## INSTALL
- rpm -Uvh https://download.fmi.fi/smartmet-open/rhel/7/x86_64/smartmet-open-release-17.9.28-1.el7.fmi.noarch.rpm
- yum install smartmet-data-sounding-ra4

## BUILD RPM
- cd $HOME/rpmbuild/SOURCES/
- git clone https://github.com/fmidev/smartmet-data-sounding-ra4.git
- rpmbuild -ba smartmet-data-sounding-ra4/smartmet-data-sounding-ra4.spec
