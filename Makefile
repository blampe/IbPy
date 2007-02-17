version := 0.7
revision := `svnversion|cut -f 2 -d \:|cut -f 1 -d M`

twsapitxt := ib/ext/src/IBJts/API_VersionNum.txt
version_api := `cat $(twsapitxt) |cut -f 2 -d \=`


release_dir := release-$(version).$(version_api)


.PHONY: all release sdist

all: release sdist

release:
	rm -rf $(release_dir)
	@echo building release for version=$(version) revision=$(revision)

sdist:
	svn export http://ibpy.melhase.net/repos/branches/ast $(release_dir) > /dev/null
	cd $(release_dir)
	cd $(release_dir)/ib && sed -i s/tws_api_version\ \=\ "0"/tws_api_version\ \=\ \"`cat $(twsapitxt) |cut -f 2 -d \=`\"/ __init__.py
	cd $(release_dir)/ib && sed -i s/version\ \=\ "0"/version\ \=\ \"`cat $(twsapitxt) |cut -f 2 -d \=`\"/ __init__.py
	cd $(release_dir)/ib && sed -i s/revision\ \=\ "r0"/revision\ \=\ \"r$(svnrev)\"/ __init__.py

	@echo cd $(release_dir) setup.py sdist
