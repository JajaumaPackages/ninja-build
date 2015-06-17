Name:           ninja-build
Version:        1.5.3
Release:        4%{?dist}
Summary:        A small build system with a focus on speed
License:        ASL 2.0
URL:            http://martine.github.com/ninja/
Source0:        https://github.com/martine/ninja/archive/v%{version}.tar.gz#/ninja-%{version}.tar.gz
Source1:        ninja.vim
# https://github.com/martine/ninja/pull/882
Patch0:         ninja-1.5.3-verbose-build.patch
BuildRequires:  asciidoc
BuildRequires:  gtest-devel
BuildRequires:  python2-devel
BuildRequires:  re2c >= 0.11.3
Requires:       emacs-filesystem
Requires:       vim-filesystem

%description
Ninja is a small build system with a focus on speed. It differs from other
build systems in two major respects: it is designed to have its input files
generated by a higher-level build system, and it is designed to run builds as
fast as possible.

%prep
%setup -qn ninja-%{version}
%patch0 -p1 -b .verbose-build

%build
CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" \
%{__python2} configure.py --bootstrap --verbose
./ninja -v manual
./ninja -v ninja_test

%install
# TODO: Install ninja_syntax.py?
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}/bash-completion/completions,%{_datadir}/emacs/site-lisp,%{_datadir}/vim/vimfiles/syntax,%{_datadir}/vim/vimfiles/ftdetect,%{_datadir}/zsh/site-functions}

install -pm755 ninja %{buildroot}%{_bindir}/ninja-build
install -pm644 misc/bash-completion %{buildroot}%{_datadir}/bash-completion/completions/ninja-bash-completion
install -pm644 misc/ninja-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/ninja-mode.el
install -pm644 misc/ninja.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/ninja.vim
install -pm644 %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/ninja.vim
install -pm644 misc/zsh-completion %{buildroot}%{_datadir}/zsh/site-functions/_ninja

%check
# workaround possible too low default limits
ulimit -n 2048 && ulimit -u 2048
./ninja_test

%files
%doc COPYING HACKING.md README doc/manual.html
%{_bindir}/ninja-build
%{_datadir}/bash-completion/completions/ninja-bash-completion
%{_datadir}/emacs/site-lisp/ninja-mode.el
%{_datadir}/vim/vimfiles/syntax/ninja.vim
%{_datadir}/vim/vimfiles/ftdetect/ninja.vim
# zsh does not have a -filesystem package
%{_datadir}/zsh/

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.3-3
- Rebuilt for GCC 5 C++11 ABI change

* Sun Feb 08 2015 Ben Boeckel <mathstuf@gmail.com> - 1.5.3-2
- Update bash-completions location

* Wed Dec 10 2014 Ben Boeckel <mathstuf@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Christopher Meng <rpm@cicku.me> - 1.5.1-1
- Update to 1.5.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Ben Boeckel <mathstuf@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Sun Nov  3 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.3.4-4
- Use special %%doc to install all docs (#994005).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Dan Horák <dan[at]danny.cz> - 1.3.4-2
- workaround possible too low limits for number of processes and open files,
  fixes build on ppc/ppc64 and s390(x)

* Sun Jun 09 2013 Ben Boeckel <mathstuf@gmail.com> - 1.3.4-1
- Update to 1.3.4
- Run test suite

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Ben Boeckel <mathstuf@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Thu Jul 19 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.6.20120719git5dc55a3
- Update to new snapshot

* Mon Jul 09 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.5.20120709gitb90d038
- Preserve timestamps on install
- Install as ninja-build to avoid conflicts with the ninja IRC package
- Update snapshot

* Tue Jun 19 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.4.20120605git54553d3
- Add an ftdetect file for ninja
- Fix zsh-stuff directory ownership

* Thu Jun 07 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.3.20120605git54553d3
- Add a Group tag

* Tue Jun 05 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.2.20120605git54553d3
- Update to new snapshot

* Fri Mar 30 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.1.20120330gitabd33d5
- Initial package
