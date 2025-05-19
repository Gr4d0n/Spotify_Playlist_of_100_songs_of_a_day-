from bs4 import BeautifulSoup
import requests


class SongList():
    def __init__(self):
        self.date = None

    def create_TSOTD(self):
        self.date = input("Date in format YYYY-MM-DD: ")
        billboard_data = requests.get(f"https://www.billboard.com/charts/hot-100/{self.date}/", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}).text

        soup = BeautifulSoup(billboard_data, "html.parser")
        top_song_titles = soup.select('li.lrv-u-width-100p h3#title-of-a-story')

        with open(f"top_songs_{self.date}.txt", 'w') as file:
            a = 1
            for song in top_song_titles:
                file.write(f'{a}. {song.getText().strip()}\n')
                a += 1
