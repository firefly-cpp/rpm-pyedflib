# configuration problems in upstream's config
%bcond_with docs

%global pretty_name pyedflib

%global _description %{expand:
pyEDFlib is a python library to read/write EDF+/BDF+ files based on EDFlib.
EDF means European Data Format and was firstly published Kemp1992. 
In 2003, an improved version of the file protocol named EDF+ has 
been published and can be found at Kemp2003.}

Name:           python-%{pretty_name}
Version:        0.1.22
Release:        1%{?dist}
Summary:        Python library to read/write EDF+/BDF+ files, based on EDFlib 

License:        BSD
URL:            https://github.com/holgern/%{pretty_name}
Source0:        %{url}/archive/v%{version}/%{pretty_name}-%{version}.tar.gz

# Use default Fedora version of numpy in order to avoid complications
Patch0:         0001-Use-default-numpy-version.patch

# Uses a forked copy of EDFlib (https://gitlab.com/Teuniz/EDFlib), which has
# elected not to support big-endian architectures.
ExcludeArch:    s390x

# Uses a forked copy of EDFlib (https://gitlab.com/Teuniz/EDFlib)
# https://github.com/holgern/pyedflib/issues/149
# Version number: pyedflib/_extensions/c/edflib.c, EDFLIB_VERSION
Provides:       bundled(edflib) = 1.17

%description %_description

%package -n python3-%{pretty_name}
Summary:        %{summary}

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

#For documentation
%if %{with docs}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
%endif

%description -n python3-%{pretty_name} %_description

%if %{with docs}
%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.
%endif

%prep
%autosetup -p1 -n %{pretty_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%if %{with docs}
PYTHONPATH=".:.." make -C doc SPHINXOPTS=%{?_smp_mflags} SPHINXBUILD=sphinx-build-3 html
rm -rf doc/_build/html/{.doctrees,.buildinfo} -vf
%endif

%install
%pyproject_install
%pyproject_save_files pyedflib

%check
%tox

%files -n python3-%{pretty_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%if %{with docs}
%files doc
%license LICENSE
%doc doc/_build/html
%endif

%changelog
%autochangelog
