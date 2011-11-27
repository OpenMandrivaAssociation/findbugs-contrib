%global plugin_dir %{_datadir}/findbugs/plugin
%global eclipse_plugin_vers 1.3.9
%global eclipse_plugin_date 20090821
%global eclipse_plugins_dir %{_datadir}/eclipse/dropins/findbugs/plugins
%global eclipse_plugin_dir  %{eclipse_plugins_dir}/edu.umd.cs.findbugs.plugin.eclipse_%{eclipse_plugin_vers}.%{eclipse_plugin_date}

Name:           findbugs-contrib
Version:        4.2.0
Release:        5
Summary:        Extra findbugs detectors

Group:          Development/Java
License:        LGPLv2+
URL:            http://fb-contrib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/fb-contrib/fb-contrib-src-%{version}.zip
# This patch has not been submitted upstream, as it contains Fedora-specific
# changes.  It looks in /usr/share/java for jar files at both compile time and
# run time, instead of using the jars in lib/.
Patch0:         findbugs-contrib-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  ant-nodeps, findbugs, java-1.6.0-openjdk-devel, jpackage-utils
BuildRequires:  jsp21, junit4, log4j, servlet25
Requires:       findbugs, java-1.6.0-openjdk, jpackage-utils

%description
This is an extra detector plugin to be used with the static bug finder
FindBugs.  See the documentation for descriptions of the detectors.

%package javadoc
Group:          Development/Java
Summary:        Javadoc documentation for %{name}
Requires:       %{name} = %{version}-%{release}

%description javadoc
Javadoc documentation for %{name}.

%package samples
Group:          Development/Java
Summary:        Sample input files illustrating the detectors
Requires:       %{name} = %{version}-%{release}, jsp21, junit4, log4j, servlet25

%description samples
This package contains sample input files that illustrate the various findbugs
detectors.

%package -n eclipse-findbugs-contrib
Group:          Development/Java
Summary:        Eclipse plugin for findbugs-contrib
Requires:       %{name} = %{version}-%{release}
Requires:       eclipse-findbugs = %{eclipse_plugin_vers}

%description -n eclipse-findbugs-contrib
This package integrates the findbugs-contrib detectors into Eclipse, in
addition to the base findbugs detectors.

%prep
%setup -q -c
%patch0

# Remove the precompiled files
rm -fr classes/com fb-contrib-*.jar lib/* samples/*.class samples/lib/*.jar

# Remove the duplicated sources (!)
rm -fr com

%build
ant build
ant javadoc

%install
rm -rf $RPM_BUILD_ROOT

# Install the plugin
mkdir -p $RPM_BUILD_ROOT%{plugin_dir}
cp -p fb-contrib-%{version}.jar $RPM_BUILD_ROOT%{plugin_dir}

# Install the documentation
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/fb-contrib-%{version}
cp -a javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/fb-contrib-%{version}
ln -s fb-contrib-%{version} $RPM_BUILD_ROOT%{_javadocdir}/fb-contrib

# Make a soft link for eclipse
mkdir -p $RPM_BUILD_ROOT%{eclipse_plugin_dir}
ln -s %{plugin_dir}/fb-contrib-%{version}.jar \
  $RPM_BUILD_ROOT%{eclipse_plugin_dir}/fb-contrib-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc license.txt htdocs/*
%{plugin_dir}/fb-contrib-%{version}.jar

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*

%files samples
%defattr(-,root,root,-)
%doc samples/*

%files -n eclipse-findbugs-contrib
%defattr(-,root,root,-)
%{eclipse_plugin_dir}/fb-contrib-%{version}.jar

