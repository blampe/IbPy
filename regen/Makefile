
javafiles := `find "$(TWS_HOME)/java/com/ib/client" -name "*.java"`
javasources := $(wordlist 1,$(words $(javafiles)),$(javafiles))


.PHONY: all clean lib src


all: lib src


clean:
	rm -f *.pyo
	rm -f *.pyc
	cd lib && $(MAKE) clean
	cd src && $(MAKE) clean

lib:
	cd lib && $(MAKE)

src:
	cd src && $(MAKE)
