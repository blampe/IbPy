ibsources_jar := twsapi_unixmac_967.jar
ibsources_url := "http://www.interactivebrokers.com/download/$(ibsources_jar)"


.PHONY: all clean


all: $(ibsources_jar) IBJts


$(ibsources_jar):
	wget $(ibsources_url)


IBJts:
	jar -xf $(ibsources_jar)

clean:
	rm $(ibsources_jar)
	rm -rf IBJts
