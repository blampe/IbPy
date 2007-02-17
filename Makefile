ibpy_ver    := 0.7.0
ibpy_rev    := $(shell svnversion|cut -f 2 -d \:|cut -f 1 -d M)
twsapi_ver  := $(shell cat ib/ext/src/IBJts/API_VersionNum.txt |cut -f 2 -d \=)
release_num := $(ibpy_ver)-$(twsapi_ver)
release_dir := release-$(release_num)
svn_root    := http://ibpy.melhase.net/repos/branches/ast

.PHONY: all release sdist


all: release sdist


release:
	@echo removing previous release dir
	@rm -rf $(release_dir)
	@echo building release=$(release_num) version=$(ibpy_ver) revision=$(ibpy_rev) api=$(twsapi_ver)

sdist:
	@echo exporting trunk from $(svn_root) into $(release_dir)
	@svn export $(svn_root) $(release_dir) > /dev/null
	@echo fixing version strings
	@cd $(release_dir)/ib && sed -i s/api\ \=\ \"0\"/api\ \=\ \"$(twsapi_ver)\"/ __init__.py
	@cd $(release_dir)/ib && sed -i s/version\ \=\ \"0\"/version\ \=\ \"$(release_num)\"/ __init__.py
	@cd $(release_dir)/ && sed -i s/version\ \=\ \"0\"/version\ \=\ \"$(release_num)\"/ setup.py
	@cd $(release_dir)/ib && sed -i s/revision\ \=\ \"r0\"/revision\ \=\ \"r$(ibpy_rev)\"/ __init__.py
	@echo building source distribution
	@echo cd $(release_dir) setup.py sdist
