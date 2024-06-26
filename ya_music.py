import os, sys
import datetime
import json

from yandex_music import Client, DownloadInfo

def func() -> str:
    # без автор изации недоступен список треков альбома
    TOKEN = 'AgAAAAAapMjmAAG8XoVimyhj_0DLqVoduiy3Zl8'

    client = Client(TOKEN).init()
    history = client.account_status().rec
    for i in client.users_playlists(kind='history'):
        print(i)
        break
    
    return "bbb"
    # playlist = client.users_likes_tracks()
    # arr = []

    # for i in playlist:
    #     # print(i.fetch_track().title)
    #     time = datetime.datetime.strptime(i['timestamp'][:-6], '%Y-%m-%dT%H:%M:%S')
    #     arr = [time, i['album_id'], i['id'], i.fetch_track().title]
    #     break

    # # arr.sort(reverse=True)

    # for i in client.tracks_download_info(arr[2], True):
    #     print(i)
    #     if i["codec"] == "mp3":
    #         return i["direct_link"]

func()

sys.exit(0)


tracks = []
for i, volume in enumerate(album.volumes):
    if len(album.volumes) > 1:
        tracks.append(f'💿 Диск {i + 1}')
    tracks += volume

text = 'АЛЬБОМ\n\n'
text += f'{album.title}\n'
text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
text += f'{album.year} · {album.genre}\n'

cover = album.cover_uri
if cover:
    text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

text += 'Список треков:'

print(text)

for track in tracks:
    if isinstance(track, str):
        print(track)
    else:
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)
        print(track.title + artists)