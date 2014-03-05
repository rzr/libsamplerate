#
# spec file for package libsamplerate
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           libsamplerate
Version:        0.1.8
Release:        0
Summary:        A Sample Rate Converter Library
License:        GPL-2.0+
Group:          System/Libraries
Url:            http://www.mega-nerd.com/SRC/
Source0:        http://www.mega-nerd.com/SRC/libsamplerate-%{version}.tar.gz
Source1001:     libsamplerate.manifest
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# PATCH-FIX-UPSTREAM 0001-src-src_sinc.c-Fix-a-read-beyond-end-of-coefficent-a.patch off by one in src_sinc
#Patch:          0001-src-src_sinc.c-Fix-a-read-beyond-end-of-coefficent-a.patch

%description
Secret Rabbit Code (aka libsamplerate) is a Sample Rate Converter for
audio. One example of where such a thing would be useful is in
converting audio from the CD sample rate of 44.1kHz to the 48kHz sample
rate used by DAT players.

SRC is capable of arbitrary and time varying conversions; from
downsampling by a factor of 12 to upsampling by the same factor.  The
conversion ratio can also vary with time for speeding up and slowing
down effects.

%package -n libsamplerate0
Summary:        A Sample Rate Converter Library
Group:          System/Libraries

%description -n libsamplerate0
Secret Rabbit Code (aka libsamplerate) is a Sample Rate Converter for
audio. One example of where such a thing would be useful is in
converting audio from the CD sample rate of 44.1kHz to the 48kHz sample
rate used by DAT players.

SRC is capable of arbitrary and time varying conversions; from
downsampling by a factor of 12 to upsampling by the same factor.  The
conversion ratio can also vary with time for speeding up and slowing
down effects.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Languages
Requires:       glibc-devel
Requires:       libsamplerate0 = %{version}

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package progs
Summary:        Example Programs for libsamplerate
Group:          Multimedia/Utilities

%description progs
This package includes the example programs for libsamplerate.

%prep
%setup -q

cp %{SOURCE1001} .

%build
%ifnarch %arm aarch64
# ARM has no working profile support in gcc atm
profiledir=`mktemp -d`
export CFLAGS="%optflags %cflags_profile_generate=$profiledir"
%configure --disable-silent-rules --disable-static
make %{?_smp_mflags}
pushd tests
popd
make clean
export CFLAGS="%optflags %cflags_profile_feedback=$profiledir"
%else
export CFLAGS="%optflags"
%endif
%configure --disable-silent-rules --disable-static --disable-fftw
make %{?_smp_mflags}

%check
pushd tests
make check
popd

%install
# Since configure doesn't honor --docdir set htmldocdir here
make install DESTDIR=%{?buildroot} \
             htmldocdir=%{_defaultdocdir}/libsamplerate-devel
# remove unneeded files
rm -f %{buildroot}%{_libdir}/*.la

%post -n libsamplerate0 -p /sbin/ldconfig
%postun -n libsamplerate0 -p /sbin/ldconfig

%files -n libsamplerate0
%defattr(-,root,root)
%doc AUTHORS
%license COPYING
%{_libdir}/libsamplerate.so.0*

%files devel
%defattr(-,root,root)
%doc ChangeLog
%{_defaultdocdir}/libsamplerate-devel
%{_libdir}/libsamplerate.so
%{_includedir}/samplerate.h
%{_libdir}/pkgconfig/samplerate.pc

%files progs
%defattr(-,root,root)
%{_bindir}/sndfile-resample
