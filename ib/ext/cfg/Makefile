configs := $(addsuffix .py, $(notdir $(basename $(wildcard ../src/IBJts/source/JavaClient/com/ib/client/*.java))))

.PHONY: all clean


all: $(configs)


$(configs):
	touch $@

clean:
	rm -rf *.pyo
	rm -rf *.pyc
