all:

data:
	python3 src/data/scrapper/scrapper.py
	python3 src/data/scrapper/scrapperStadium.py
	python3 src/data/scrapper/scrapperPlayers.py
	python3 src/data/purify/stadiumPurify.py
	python3 src/data/features/gameFeatures.py
	python3 src/data/features/timePlayed.py
	python3 src/data/features/individualActivity.py

test:
	python3 test/test.py

clean:
	find ./data -name "*.txt" -type f -delete
	find ./data -name "*.csv" -type f -delete

