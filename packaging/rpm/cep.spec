Name:     cep
Version:  %{__version}
Release:  %{__release}%{?dist}

License:  GNU AGPLv3
URL:  https://github.com/redBorder/cep.git
Source0: %{name}-%{version}.tar.gz

BuildRequires: maven java-devel

Summary: redborder Complex Event Processor
Group: Services/Monitoring/Correlation
Requires: java

%description
%{summary}

%prep
%setup -qn %{name}-%{version}

%build
mvn clean package

%install
mkdir -p %{buildroot}/usr/lib/%{name}
install -D -m 644 target/cep-*-selfcontained.jar %{buildroot}/usr/lib/%{name}
mv %{buildroot}/usr/lib/%{name}/cep-*-selfcontained.jar %{buildroot}/usr/lib/%{name}/cep.jar
install -D -m 644 src/main/resources/log4j2_demo.xml %{buildroot}/etc/%{name}/log4j2_demo.xml
install -D -m 644 cep.service %{buildroot}/usr/lib/systemd/system/cep.service

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d / -s /sbin/nologin \
    -c "User of %{name} service" %{name}
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root)
/usr/lib/%{name}
/etc/%{name}/log4j2_demo.xml
/usr/lib/systemd/system/cep.service

%changelog
* Fri Jun 17 2016 Carlos J. Mateos  <cjmateos@redborder.com> - 1.0.0-1
- first spec version
