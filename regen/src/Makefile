ibsources_jar := twsapi_unixmac.jar
ibsources_url := "http://www.interactivebrokers.com/download/$(ibsources_jar)"


.PHONY: all clean


all: $(ibsources_jar) IBJts


$(ibsources_jar):
	wget $(ibsources_url)

IBJts:
	jar -xf $(ibsources_jar) IBJts/java/com/ IBJts/API_VersionNum.txt

clean:
	@echo
