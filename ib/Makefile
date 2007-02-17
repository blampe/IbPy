svnrev := `svnversion|cut -f 2 -d \:|cut -f 1 -d M`
twsapitxt := ext/src/IBJts/API_VersionNum.txt

.PHONY: all clean __init__.py


all: ext $(twsapitxt) __init__.py

ext:
	cd ext && $(MAKE)

$(twsapitxt):
	cd ext/src && $(MAKE) IBJts

__init__.py: $(twsapitxt)
	sed -i s/tws_api_version\ \=\ .*/tws_api_version\ \=\ \"`cat $(twsapitxt) |cut -f 2 -d \=`\"/ __init__.py
	sed -i s/revision\ \=\ .*/revision\ \=\ \"r$(svnrev)\"/ __init__.py

clean:
	rm -f *.pyo
	rm -f *.pyc
	cd ext && $(MAKE) clean
