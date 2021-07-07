# Twitch VOD Library

The Twitch VOD Library is a web app that lets you save and organize links to VODs or clips from the streaming website [Twitch](https://www.twitch.tv/). It allows you to add new clips (clips.twitch/tv/) or VODs (twitch.tv/videos/) by simply entering the full link. All of the information about it gets written to your local database, which you can then view in the browser. You also have the possibilty to give each individual entry a star or a checkmark, and you can also delete entries. It is furthermore possible to sort entries by various different metrics.

## Getting Started

1. Download this entire repo and extract it to a folder
2. Run "START.bat"
3. Go to localhost:8888 in your browser (or use the ip address of your device and the port 8888)

## Built With

* [Selenium WebDriver](https://www.selenium.dev/) - Web Scraping framework, which was used for getting all the relevant data from Twitch
* [FastAPI](https://fastapi.tiangolo.com/) - Python module which was used to build an API that connects the frontend and the backend, which in turn is connected to the database