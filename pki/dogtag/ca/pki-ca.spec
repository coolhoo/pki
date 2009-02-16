# BEGIN COPYRIGHT BLOCK
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# (C) 2007 Red Hat, Inc.
# All rights reserved.
# END COPYRIGHT BLOCK

###############################################################################
###                          D E F I N I T I O N S                          ###
###############################################################################

## Entity Definitions
%define base_entity       Dogtag
%define base_flavor       dogtag
%define base_prefix       pki

## Product Definitions
%define base_system       Certificate System
%define base_product      Certificate Authority
%define base_component    ca
%define base_pki          %{base_entity} %{base_system}

## Package Header Definitions
%define base_name         %{base_prefix}-%{base_component}
%define base_version      1.0.0
%define base_release      25
%define base_group        System Environment/Daemons
%define base_vendor       Red Hat, Inc.
%define base_license      GPLv2 with exceptions
%define base_packager     %{base_vendor} <http://bugzilla.redhat.com/bugzilla>
%define base_summary      %{base_pki} - %{base_product}
%define base_url          http://pki.fedoraproject.org/wiki/PKI_Documentation

## Pre & Post Install/Uninstall Scripts Definitions
%define base_user         pkiuser
%define base_instance     /var/lib/%{base_name}

## Helper Definitions
%define pki_jdk           java-devel >= 1:1.6.0
# Override the default 'pki_jdk' on Fedora 8 platforms
%{?fc8:%define pki_jdk    java-devel >= 1.7.0}
%define pki_ca            %{base_entity} Certificate Authority
%define pki_drm           %{base_entity} Data Recovery Manager
%define pki_ds            Fedora Directory Server
%define pki_ocsp          %{base_entity} Online Certificate Status Protocol Manager
%define pki_ra            %{base_entity} Registration Authority
%define pki_tks           %{base_entity} Token Key Service
%define pki_tps           %{base_entity} Token Processing System

## Don't build the debug packages
%define debug_package     %{nil}


##===================##
## Linux Definitions ##
##===================##
%ifos Linux
## For PKI version information, ALWAYS refer to the version of the
## Dogtag UI package dependency associated with this Dogtag spec file!
%define pki_version       %(echo `rpm -q --queryformat '%{VERSION}' %{base_flavor}-%{base_name}-ui`)
%define pki_major_version %(echo `echo %{pki_version} | awk -F. '{ print $1 }'`)
%define pki_minor_version %(echo `echo %{pki_version} | awk -F. '{ print $2 }'`)
%define pki_patch_version %(echo `echo %{pki_version} | awk -F. '{ print $3 }'`)

## Disallow an initial login shell
## NOTE:  SELinux policy requires a shell of /sbin/nologin
%define base_login_shell  /sbin/nologin

## A distribution model is required on certain Linux operating systems!
##
## check for a pre-defined distribution model
%define undefined_distro  %(test "%{dist}" = "" && echo 1 || echo 0)
%if %{undefined_distro}
%define is_fedora         %(test -e /etc/fedora-release && echo 1 || echo 0)
%if %{is_fedora}
## define a default distribution model on Fedora Linux
%define dist_prefix       .fc
%define dist_version      %(echo `rpm -qf --qf='%{VERSION}' /etc/fedora-release` | tr -d [A-Za-z])
%define dist              %{dist_prefix}%{dist_version}
%else
%define is_redhat         %(test -e /etc/redhat-release && echo 1 || echo 0)
%if %{is_redhat}
## define a default distribution model on Red Hat Linux
%define dist_prefix       .el
%define dist_version      %(echo `rpm -qf --qf='%{VERSION}' /etc/redhat-release` | tr -d [A-Za-z])
%define dist              %{dist_prefix}%{dist_version}
%endif
%endif
%endif
%endif



###############################################################################
###                       P A C K A G E   H E A D E R                       ###
###############################################################################

Name:           %{base_name}
Version:        %{base_version}
Release:        %{base_release}%{?dist}
Summary:        %{base_summary}
Vendor:         %{base_vendor}
URL:            %{base_url}
License:        %{base_license}
Packager:       %{base_packager}
Group:          %{base_group}


## Without AutoReqProv: no, rpmbuild finds all sorts of crazy
## dependencies that we don't care about, and refuses to install
AutoReqProv:    no

BuildArch:      noarch
BuildRoot:      %{_builddir}/%{base_name}-root


## NOTE:  This spec file may require a specific JDK, "gcc", and/or "gcc-c++"
##        packages as well as the "rpm" and "rpm-build" packages.
##
##        Technically, "ant" should not need to be in "BuildRequires" since
##        it is the Java equivalent of "make" (and/or "Autotools").
##
BuildRequires:  ant >= 1.6.2, %{base_flavor}-%{base_name}-ui >= 1.0.0, %{base_prefix}-common >= 1.0.0, %{base_prefix}-util >= 1.0.0, %{pki_jdk}, jpackage-utils >= 1.6.0, jss >= 4.2.5, tomcatjss >= 1.1.0

## Without Requires something, rpmbuild will abort!
Requires:       %{base_name}-ui, %{base_prefix}-common >= 1.0.0, %{base_prefix}-selinux >= 1.0.0


## This package is non-relocatable!
#Prefix:

Source0:        %{base_name}-%{base_version}.tar.gz

## This package currently contains no patches!
#Patch0:


%description
%{base_pki} is an enterprise software system designed
to manage enterprise Public Key Infrastructure (PKI) deployments.

The %{pki_ca} is a required PKI subsystem which issues,
renews, revokes, and publishes certificates as well as compiling and
publishing Certificate Revocation Lists (CRLs).
The %{pki_ca} can be configured as a self-signing
Certificate Authority (CA), where it is the root CA, or it can act as a
subordinate CA, where it obtains its own signing certificate from a public CA.



###############################################################################
###                  P R E P A R A T I O N   &   S E T U P                  ###
###############################################################################

## On Linux systems, prep and setup expect there to be a Source file
## in the /usr/src/redhat/SOURCES directory - it will be unpacked
## in the _builddir (not BuildRoot)
%prep


%setup -q


## This package currently contains no patches!
#%patch0
# patches



###############################################################################
###                        B U I L D   P R O C E S S                        ###
###############################################################################

%build
ant -Dspecfile=%{base_name}.spec



###############################################################################
###                 I N S T A L L A T I O N   P R O C E S S                 ###
###############################################################################

%install
cd dist/binary
unzip %{name}-%{version}.zip -d ${RPM_BUILD_ROOT}
sed -i 's/^preop.product.version=.*$/preop.product.version=%{pki_version}/' ${RPM_BUILD_ROOT}/usr/share/%{base_prefix}/%{base_component}/conf/CS.cfg
sed -i 's/^cms.version=.*$/cms.version=%{pki_major_version}.%{pki_minor_version}/' ${RPM_BUILD_ROOT}/usr/share/%{base_prefix}/%{base_component}/conf/CS.cfg
cd ${RPM_BUILD_ROOT}/usr/share/java/%{base_prefix}/%{base_component}
mv %{base_component}.jar %{base_component}-%{version}.jar
ln -s %{base_component}-%{version}.jar %{base_component}.jar



###############################################################################
###                      C L E A N U P   P R O C E S S                      ###
###############################################################################

%clean
rm -rf ${RPM_BUILD_ROOT}



###############################################################################
###  P R E  &  P O S T   I N S T A L L / U N I N S T A L L   S C R I P T S  ###
###############################################################################

%pre
if [ `grep -c %{base_user} /etc/group` -eq 0 ] ; then
	echo "Adding default PKI group \"%{base_user}\" to /etc/group."
	groupadd %{base_user}
fi
if [ `grep -c %{base_user} /etc/passwd` -eq 0 ] ; then
	echo "Adding default PKI user \"%{base_user}\" to /etc/passwd."
	useradd -g %{base_user} -d %{_datadir}/%{base_prefix} -s %{base_login_shell} -c "%{base_pki}" -m %{base_user}
fi


%post
chmod 00755 %{_datadir}/%{base_prefix}/%{base_component}/setup/postinstall
%{_datadir}/%{base_prefix}/%{base_component}/setup/postinstall %{base_prefix} %{base_component} %{base_version} %{base_release}
echo ""
echo "Install finished."


%preun
if [ -d %{base_instance} ] ; then
	echo "WARNING:  The default instance \"%{base_instance}\" was NOT removed!"
	echo ""
	echo "NOTE:  This means that the data in the default instance called"
	echo "       \"%{base_instance}\" will NOT be overwritten once the"
	echo "       \"%{name}\" package is re-installed."
	echo ""
	echo "Shutting down the default instance \"%{base_instance}\""
	echo "PRIOR to uninstalling the \"%{name}\" package:"
	echo ""
	/etc/init.d/%{base_name} stop
fi


## This package currently contains no post-uninstallation process!
#%postun



###############################################################################
###   I N V E N T O R Y   O F   F I L E S   A N D   D I R E C T O R I E S   ### 
###############################################################################

%files
%attr(-,root,root)     %{_datadir}/doc/%{base_name}-%{base_version}/*
%attr(-,root,root)     %{_datadir}/java/%{base_prefix}/%{base_component}
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/acl
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/alias
%attr(00660,root,root) %{_datadir}/%{base_prefix}/%{base_component}/conf/CS.cfg
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/conf/[a-z]*
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/emails
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/etc
%attr(00770,root,root) %{_datadir}/%{base_prefix}/%{base_component}/logs/signedAudit
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/profiles
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/setup
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/shared
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/temp
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/webapps
%attr(-,root,root)     %{_datadir}/%{base_prefix}/%{base_component}/work



###############################################################################
###                            C H A N G E L O G                            ###
###############################################################################

%changelog
* Mon Feb 16 2009 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-25
- Bugzilla Bug #485790 -  Need changes made to spec files in various
  packages to be able to build in koji/brew
* Sat Feb 14 2009 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-24
- Bugzilla Bug #250874 -Change spec file dependencies to rely on latest
  versions of components (NSPR, NSS, JSS, MOD_NSS)
* Thu Feb 12 2009 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-23
- Bugzilla Bug #483699 -  problem with the epoch in the spec file causes
  build to fail
* Wed Feb 11 2009 Ade Lee <alee@redhat.com> 1.0.0-22
- Bugzilla Bug 443413 - Email response template contains wrong link
* Tue Jan 27 2009 Ade Lee <alee@redhat.com> 1.0.0-21
- Bugzilla Bug 480679 - Integrate selinux into framework
* Thu Jan 22 2009 Christina Fu <cfu@redhat.com> 1.0.0-20
- Bugzilla Bug 481237 - Audit Log signing framework
* Mon Jan 5 2009 Ade Lee <alee@redhat.com> 1.0.0-19
- Bugzilla Bug #472006, 472007 - Serial number management
* Wed Dec 10 2008 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-18
- Bugzilla Bug #475895 - Parameterize the initial login shell
* Fri Nov 28 2008 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-17
- Bugzilla Bug #445402 - changed "linux"/"fedora" to "dogtag"; changed
                         "pki-svn.fedora.redhat.com" to "pki.fedoraproject.org"
* Mon Nov 24 2008 Ade Lee <alee@redhat.com> 1.0.0-16
- Bugzilla Bug #237727 - selinux changes to init script
* Sat Nov 22 2008 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-15
- Bugzilla Bug #472305 - "equality" tests in all spec files need to be fixed
- Bumped "java" and "java-devel" 1.4.2 and 1.5.0 dependencies to 1.6.0
- Changed "java-sdk" to "java-devel" for consistency
* Tue Nov 18 2008 Christina Fu <cfu@redhat.com> 1.0.0-14
- Bugzilla Bug #471622 - Need Renewal feature via enrollment profile Framework (phase 1)
* Fri Oct 10 2008 Jack Magne <jmagne@redhat.com> 1.0.0-13
- Fix for port separation bug #466188.
* Fri Oct 9 2008 Ade Lee <alee@redhat.com> 1.0.0-12
- Fix for Bug 223361. Security Domains in LDAP.
* Fri Aug 8 2008 Andrew Wnuk <awnuk@redhat.com> 1.0.0-11
- Fix for Bug 453834.
* Thu Aug 7 2008 Jack Magne <jmagne@redhat.com> 1.0.0-10
- Fix for Bug #458337.
* Thu Aug 7 2008 Andrew Wnuk <awnuk@redhat.com> 1.0.0-9
- Fix for Bug 453834.
* Fri Jul 11 2008 Andrew Wnuk <awnuk@redhat.com> 1.0.0-8
- Fix for bug #243804.
* Wed Jun 25 2008 Andrew Wnuk <awnuk@redhat.com> 1.0.0-7
- Fix for bug #443687.
* Mon Jun 9 2008 Matthew Harmsen <mharmsen@redhat.com> 1.0.0-6
- Bugzilla Bug #450345:  Port Dogtag 1.0.0 to
  Fedora 9 (32-bit i386 & 64-bit x86_64).
* Fri May 16 2008 Andrew Wnuk <awnuk@redhat.com> 1.0.0-5
- Fix for bug #445470.
* Tue May 7 2008 Jack Magne   <jmagne@redhat.com> 1.0.0-4
- Fix for Bug #440079.
* Tue May 6 2008 Andrew Wnuk <awnuk@redhat.com> 1.0.0-3
- Provided CRL page size as configurable parameter - bug #445400. 
* Thu Apr 17 2008 Christina Fu <cfu@redhat.com> 1.0.0-2
- Implemented bug #442800 - support UUID in Subject Alternative Name extension.  Version 4 only, for now. 
* Tue Feb 19 2008 PKI Team <pki-devel@redhat.com> 1.0.0-1
- Initial open source version based upon proprietary
  Red Hat Certificate System (RHCS) 7.3.

