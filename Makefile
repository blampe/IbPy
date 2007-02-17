version := 0.7
revision := $(shell svnversion|cut -f 2 -d \:|cut -f 1 -d M)

twsapitxt := ib/ext/src/IBJts/API_VersionNum.txt

version_api := $(shell cat $(twsapitxt) |cut -f 2 -d \=)


release_dir := release-$(version).$(version_api)


.PHONY: all release sdist

all: release sdist

release:
	@echo removing previous release dir
	@rm -rf $(release_dir)
	@echo building release for version=$(version).$(version_api) revision=$(revision)

sdist:
	@svn export http://ibpy.melhase.net/repos/branches/ast $(release_dir) > /dev/null
	@cd $(release_dir)/ib && sed -i s/api\ \=\ \"0\"/api\ \=\ \"$(version_api)\"/ __init__.py
	@cd $(release_dir)/ib && sed -i s/version\ \=\ \"0\"/version\ \=\ \"$(version).$(version_api)\"/ __init__.py
	@cd $(release_dir)/ib && sed -i s/version\ \=\ \"0\"/version\ \=\ \"$(version).$(version_api)\"/ setup.py
	@cd $(release_dir)/ib && sed -i s/revision\ \=\ \"r0\"/revision\ \=\ \"r$(revision)\"/ __init__.py
	@echo cd $(release_dir) setup.py sdist
