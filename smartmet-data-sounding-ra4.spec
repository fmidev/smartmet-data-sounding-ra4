%define smartmetroot /smartmet

Name:           smartmet-data-sounding-ra4
Version:        17.11.8
Release:        1%{?dist}.fmi
Summary:        SmartMet Data SOUNDING RA4
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-sounding-ra4
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%{?el6:Requires: smartmet-qdconversion}
%{?el7:Requires: smartmet-qdtools}
Requires:       lbzip2
Requires:       wget

%description
TODO

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/sounding
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/tmp/data/sounding
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/sounding/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/sounding-ra4.cron <<EOF
*/20 * * * * /smartmet/run/data/sounding/bin/get_sounding_ra4.sh &> /smartmet/logs/data/sounding.log
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_sounding <<EOF
#!/bin/sh
# Clean SOUNDING data
cleaner -maxfiles 2 '_sounding.sqd' %{smartmetroot}/data/gts/sounding
cleaner -maxfiles 2 '_sounding.sqd' %{smartmetroot}/editor/in

# Clean incoming SOUNDING data older than 7 days (7 * 24 * 60 = 10080 min)
find %{smartmetroot}/data/incoming/sounding -type f -mmin +10080 -delete
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-sounding-ra4/get_sounding_ra4.sh %{buildroot}%{smartmetroot}/run/data/sounding/bin/
install -m 755 %_topdir/SOURCES/smartmet-data-sounding-ra4/dosounding.php %{buildroot}%{smartmetroot}/run/data/sounding/bin/

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/sounding-ra4.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_sounding
%attr(2775,smartmet,gts)  %dir %{smartmetroot}/data/incoming/sounding
%{smartmetroot}/*

%changelog
* Wed Nov 8 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.8-1.%{?dist}.fmi
- Initial version
