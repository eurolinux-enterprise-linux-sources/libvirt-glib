# -*- rpm-spec -*-

%define with_introspection 0
%define with_python 0
%define with_vala 0

%if 0%{?fedora} >= 15
%define with_introspection 1
%endif
%if 0%{?fedora} && 0%{?fedora} < 15
%define with_python 1
%endif
%if 0%{?rhel} > 6
%define with_introspection 1
%endif
%if 0%{?rhel} && 0%{?rhel} < 7
%define with_python 1
%endif
%define with_vala %{with_introspection}

%define libvirt_version 0.10.2

Name: libvirt-glib
Version: 0.1.7
Release: 1%{?dist}%{?extra_release}
Summary: libvirt glib integration for events
Group: Development/Libraries
License: LGPLv2+
URL: http://libvirt.org/
Source0: ftp://libvirt.org/libvirt/glib/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: glib2-devel >= 2.22.0
BuildRequires: libvirt-devel >= %{libvirt_version}
BuildRequires: python-devel
%if %{with_introspection}
BuildRequires: gobject-introspection-devel
%if 0%{?fedora} == 12
BuildRequires: gir-repository-devel
%endif
%endif
BuildRequires: libxml2-devel
# Hack due to https://bugzilla.redhat.com/show_bug.cgi?id=613466
BuildRequires: libtool
%if %{with_vala}
BuildRequires: vala-tools
%endif

%package devel
Group: Development/Libraries
Summary: libvirt glib integration for events development files
Requires: %{name} = %{version}-%{release}

%package -n libvirt-gconfig
Group: Development/Libraries
Summary: libvirt object APIs for processing object configuration

%package -n libvirt-gobject
Group: Development/Libraries
Summary: libvirt object APIs for managing virtualization hosts

%package -n libvirt-gconfig-devel
Group: Development/Libraries
Summary: libvirt object APIs for processing object configuration development files
Requires: libvirt-gconfig = %{version}-%{release}

%package -n libvirt-gobject-devel
Group: Development/Libraries
Summary: libvirt object APIs for managing virtualization hosts development files
Requires: %{name}-devel = %{version}-%{release}
Requires: libvirt-gconfig-devel = %{version}-%{release}
Requires: libvirt-gobject = %{version}-%{release}
Requires: libvirt-devel >=  %{libvirt_version}

%if %{with_python}
%package python
Group: Development/Libraries
Summary: libvirt glib integration for events python binding
%endif

%description
This package provides integration between libvirt and the glib
event loop.

%description devel
This package provides development header files and libraries for
integration between libvirt and the glib event loop.

%description -n libvirt-gconfig
This package provides APIs for processing the object configuration
data

%description -n libvirt-gconfig-devel
This package provides development header files and libraries for
the object configuration APIs.

%description -n libvirt-gobject
This package provides APIs for managing virtualization host
objects

%description -n libvirt-gobject-devel
This package provides development header files and libraries for
managing virtualization host objects

%if %{with_python}
%description python
This package provides a python module for integration between
libvirt and the glib event loop
%endif

%prep
%setup -q

%build

%if %{with_introspection}
%define introspection_arg --enable-introspection
%else
%define introspection_arg --disable-introspection
%endif
%if %{with_python}
%define python_arg --with-python
%else
%define python_arg --without-python
%endif

%configure %{introspection_arg} %{python_arg}
%__make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%__make install  DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-glib-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-glib-1.0.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gconfig-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gconfig-1.0.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gobject-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gobject-1.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n libvirt-gconfig -p /sbin/ldconfig

%postun -n libvirt-gconfig -p /sbin/ldconfig

%post -n libvirt-gobject -p /sbin/ldconfig

%postun -n libvirt-gobject -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS ChangeLog NEWS
%{_libdir}/libvirt-glib-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGLib-1.0.typelib
%endif
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi
%endif

%files -n libvirt-gconfig
%{_libdir}/libvirt-gconfig-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGConfig-1.0.typelib
%endif
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi
%endif

%files -n libvirt-gobject
%{_libdir}/libvirt-gobject-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGObject-1.0.typelib
%endif
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi
%endif

%files devel
%defattr(-,root,root,-)
%doc examples/event-test.c
%{_libdir}/libvirt-glib-1.0.so
%{_libdir}/pkgconfig/libvirt-glib-1.0.pc
%dir %{_includedir}/libvirt-glib-1.0
%dir %{_includedir}/libvirt-glib-1.0/libvirt-glib
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib.h
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGLib-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-glib

%files -n libvirt-gconfig-devel
%defattr(-,root,root,-)
%doc examples/event-test.c
%{_libdir}/libvirt-gconfig-1.0.so
%{_libdir}/pkgconfig/libvirt-gconfig-1.0.pc
%dir %{_includedir}/libvirt-gconfig-1.0
%dir %{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig.h
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGConfig-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-gconfig

%files -n libvirt-gobject-devel
%defattr(-,root,root,-)
%doc examples/event-test.c
%{_libdir}/libvirt-gobject-1.0.so
%{_libdir}/pkgconfig/libvirt-gobject-1.0.pc
%dir %{_includedir}/libvirt-gobject-1.0
%dir %{_includedir}/libvirt-gobject-1.0/libvirt-gobject
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject.h
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGObject-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-gobject

%if %{with_python}
%files python
%defattr(-,root,root,-)
%doc examples/event-test.py
%{_libdir}/python*/site-packages/libvirtglib.py*
%{_libdir}/python*/site-packages/libvirtglibmod*
%endif

%changelog
* Mon Jul  8 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.7-1
- Update to 0.1.7 release

* Mon Mar 18 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.6-1
- Update to 0.1.6 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.5-1
- Update to 0.1.5 release

* Fri Nov 16 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.4-1
- Update to 0.1.4 release

* Mon Oct  8 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.3-1
- Update to 0.1.3 release

* Mon Aug 20 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.2-1
- Update to 0.1.2 release

* Tue Aug  7 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.1-1
- Update to 0.1.1 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-1
- Update to 0.1.0 release

* Mon Jun 25 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.9-1
- Update to 0.0.9 release

* Wed May 16 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.0.8-2
- Bump release number (no build pushed until there are more useful changes
  in there)
- Fixed conditional to ensure vala bindings are built for Fedora >= 15
  and for RHEL > 6

* Fri Apr 27 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.8-1
- Update to 0.0.8 release

* Fri Mar 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.7-1
- Update to 0.0.7 release

* Tue Mar 06 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.0.6-1
- Update to 0.0.6 release

* Mon Feb 20 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.5-1
- Update to 0.0.5 release

* Thu Jan 12 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.4-1
- Update to 0.0.4 release

* Mon Dec 19 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-1
- Update to 0.0.3 release

* Tue Nov 22 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-1
- Update to 0.0.2 release

* Tue Nov 22 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-2
- Remove gjs-devel BR
- Add missing ldconfig post/postun scripts
- Fixed conditional to ensure python is disabled for Fedora >= 15

* Mon Nov 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-1
- Initial release

