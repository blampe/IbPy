srcdir := ./src/IBJts/java/com/ib/client/
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
	j2py -i $(addprefix $(srcdir), $(addsuffix .java, $(basename $@))) -o $@ -c ib.ext.cfg -c ib.ext.cfg.$(basename $@) -s

modules-clean: clean-modules
clean-modules:
	rm -rf $(modules)
