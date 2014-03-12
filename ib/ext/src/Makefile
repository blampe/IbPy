ibsources_jar := twsapi_unixmac_969.02.jar
ibsources_url := "http://interactivebrokers.github.io/downloads/$(ibsources_jar)"


.PHONY: all clean


all: $(ibsources_jar) IBJts


$(ibsources_jar):
	wget $(ibsources_url)


IBJts:
	jar -xf $(ibsources_jar)

clean:
	rm $(ibsources_jar)
	rm -rf IBJts
