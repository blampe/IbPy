ibsources_jar := twsapi_unixmac.jar
ibsources_url := "http://www.interactivebrokers.com/download/$(ibsources_jar)"


.PHONY: all clean


all: $(ibsources_jar) IBJts


$(ibsources_jar):
	wget $(ibsources_url)


IBJts:
	jar -xf $(ibsources_jar) IBJts/java/com/ IBJts/API_VersionNum.txt
	sed -i s/tws_api_version\ \=\ .*/tws_api_version\ \=\ \"`cat IBJts/API_VersionNum.txt |cut -f 2 -d \=`\"/ ../../__init__.py


clean:
	@echo
