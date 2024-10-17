%define oname zyGrib

Summary:	Weather data visualization, GRIB file viewer
Name:		zygrib
Version:	6.2.3
Release:	3
License:	GPLv3+
Group:		Sciences/Geosciences
Url:		https://www.zygrib.org
# Sources downloaded at :
# http://www.zygrib.org/getfile.php?file=zyGrib-3.8.3.tgz
# http://www.zygrib.org/getfile.php?file=zyGrib_maps2.tgz
Source0:	%{oname}-%{version}.tgz
Source1:	%{oname}_maps2.4.tgz
# From the Debian package
Source2:	%{name}.png
Patch0:		zyGrib-6.2.3-system-qwt.patch
Patch1:		zyGrib-6.2.3-datapath.patch
BuildRequires:	bzip2-devel
BuildRequires:	libnova-devel
BuildRequires:	qt4-devel
BuildRequires:	qwt-devel
BuildRequires:	pkgconfig(proj)
Suggests:	%{name}-maps-high

%description
ZyGrib is a GRIB file viewer. It enables :

o Visualisation of meteo data from files in GRIB Format 1
o Automatic GRIB data download
o Automatic Download from IAC (fleetcode) Data
o Roh or compressed GRIB Data (gzip *.gz; bzip2 *.bz2) can be used

%files
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

#----------------------------------------------------------------------------

%package maps-high
Summary:	High resolution maps for %{oname}
Group:		Sciences/Geosciences
Requires:	%{name}
BuildArch:	noarch

%description maps-high
This package contains maps for %{oname} in higher resolution than the ones 
provided in the main package.

%files maps-high
%{_datadir}/%{name}/maps/gshhs/gshhs_0.rim
%{_datadir}/%{name}/maps/gshhs/gshhs_1.rim
%{_datadir}/%{name}/maps/gshhs/rangs_0.*
%{_datadir}/%{name}/maps/gshhs/rangs_1.*
%{_datadir}/%{name}/maps/gshhs/wdb_*_f.b
%{_datadir}/%{name}/maps/gshhs/wdb_*_h.b

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}
%setup -q -n %{oname}-%{version} -T -D -a 1
%patch0 -p1
%patch1 -p1

%build
%make

%install
install -d -m755 %{buildroot}%{_bindir}
install -D -m755 src/%{oname} %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_datadir}/%{name}/tr
cp -pr data/maps %{buildroot}%{_datadir}/%{name}/maps
cp -pr data/img %{buildroot}%{_datadir}/%{name}/img
cp -pr data/colors %{buildroot}%{_datadir}/%{name}/colors
cp -pr data/fonts %{buildroot}%{_datadir}/%{name}/fonts
cp -pr data/gis %{buildroot}%{_datadir}/%{name}/gis
cp -pr data/stuff %{buildroot}%{_datadir}/%{name}/stuff
install -D -m644 data/tr/*.qm %{buildroot}%{_datadir}/%{name}/tr

# desktop file
install -d -m755 %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Name=%{oname}
GenericName=GRIB file viewer
Comment=Weather data visualization, GRIB file viewer
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

