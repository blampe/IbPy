srcdir := ./src/IBJts/source/JavaClient/com/ib/client/
modules := $(addsuffix .py, $(notdir $(basename $(wildcard $(srcdir)*.java))))


.PHONY: all cfg clean clean-modules src


all: src cfg $(modules)


cfg:
	cd cfg && $(MAKE)


clean:
	rm -f *.pyo
	rm -f *.pyc
	cd cfg && $(MAKE) clean
	cd src && $(MAKE) clean


src:
	cd src && $(MAKE)


$(modules):
	j2py -c cfg -c cfg.$(basename $@) $(addprefix $(srcdir), $(addsuffix .java, $(basename $@))) $@

modules-clean: clean-modules
clean-modules:
	rm -rf $(modules)
