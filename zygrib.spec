%define oname	zyGrib

Name:		zygrib
Version:	5.0.6
Release:	%mkrel 1
Summary:	Weather data visualization, GRIB file viewer
License:	GPLv3
Group:		Sciences/Geosciences
Url:		http://www.zygrib.org
# Sources downloaded at :
# http://www.zygrib.org/getfile.php?file=zyGrib-3.8.3.tgz
# http://www.zygrib.org/getfile.php?file=zyGrib_maps2.tgz
# Given the size, tarballs are extracted and recompressed using xz (tar -cJ)
Source0:	%{oname}-%{version}.tgz
Source1:	%{oname}_maps2.4.tgz
# From the Debian package
Source2:	%{name}.png
Patch0:		qwt_include.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	qt4-devel libqwt-devel
BuildRequires:	proj-devel

Suggests:	%{name}-maps-high

%description
ZyGrib is a GRIB file viewer. It enables :

o Visualisation of meteo data from files in GRIB Format 1
o Automatic GRIB data download
o Automatic Download from IAC (fleetcode) Data
o Roh or compressed GRIB Data (gzip *.gz; bzip2 *.bz2) can be used

%package maps-high
Summary:	High resolution maps for %{oname}
Group:		Sciences/Geosciences

Requires:	%{name}

%description maps-high
This package contains maps for %{oname} in higher resolution than the ones 
provided in the main package.

%prep
%setup -q -n %{oname}-%{version}
%setup -q -n %{oname}-%{version} -T -D -a 1
%patch0 -p1

# fix paths so that the executable can be relocated in %{_bindir}
sed -i -e 's:"maps\/:"%{_datadir}\/%{name}\/maps\/:g' src/map/GisReader.cpp src/MainWindow.cpp
sed -i -e 's:"img\/:"%{_datadir}\/%{name}\/img\/:g' src/GribAnimator.cpp src/MenuBar.cpp
sed -i -e 's:"tr\/:"%{_datadir}\/%{name}\/tr\/:g' src/MenuBar.cpp src/main.cpp

%build
make QTBIN=%{qt4bin}

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{_bindir}
install -D -m755 src/%{oname} %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_datadir}/%{name}/tr
cp -pr data/maps %{buildroot}%{_datadir}/%{name}
cp -pr data/img %{buildroot}%{_datadir}/%{name}
install -D -m644 data/tr/*.qm %{buildroot}%{_datadir}/%{name}/tr

# desktop file
install -d -m755 %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Name=%{oname}
GenericName=GRIB file viewer
Comment=Multi-protocol Messaging Client
Exec=%{_bindir}/%{oname}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Science;Geoscience;
EOF

# icon
install -d -m755 %{buildroot}%{_datadir}/pixmaps
install -D -m644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{oname}
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/maps/gshhs/gshhs_0.rim
%exclude %{_datadir}/%{name}/maps/gshhs/gshhs_1.rim
%exclude %{_datadir}/%{name}/maps/gshhs/rangs_0.*
%exclude %{_datadir}/%{name}/maps/gshhs/rangs_1.*
%exclude %{_datadir}/%{name}/maps/gshhs/wdb_*_f.b
%exclude %{_datadir}/%{name}/maps/gshhs/wdb_*_h.b
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%files maps-high
%defattr(-,root,root,-)
%{_datadir}/%{name}/maps/gshhs/gshhs_0.rim
%{_datadir}/%{name}/maps/gshhs/gshhs_1.rim
%{_datadir}/%{name}/maps/gshhs/rangs_0.*
%{_datadir}/%{name}/maps/gshhs/rangs_1.*
%{_datadir}/%{name}/maps/gshhs/wdb_*_f.b
%{_datadir}/%{name}/maps/gshhs/wdb_*_h.b
