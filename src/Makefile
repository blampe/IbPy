ifndef TWS_HOME
$(error TWS_HOME not set)
endif

javafiles := `find "$(TWS_HOME)/java/com/ib/client" -name "*.java"`
javasources := $(wordlist 1,$(words $(javafiles)),$(javafiles))



.PHONY: all clean java


all: java


clean:
	rm -f *.pyo
	rm -f *.pyc
	cd java && $(MAKE) clean


java:
	cd java && $(MAKE)


