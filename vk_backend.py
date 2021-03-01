import requests


def parse_songs(vk_id=1):
    queries = []
    url = 'https://vk.music7s.cc/api/one_page_playlist.php?id={}&time=1614455192908&offset=0'.format(str(vk_id))
    resp = requests.get(url=url)
    data = resp.json()
    data = data['items']
    for song in data:
        if 'artist' in song.keys() and 'title' in song.keys():
            q = song['artist'] + ' - ' + song['title']
            queries.append(q)
        else:
            pass
    return list(reversed(list(set(queries))))


def get_id(short_name=''):
    url_check = "https://api.vk.com/method/users.get?user_ids=" +\
                "{}&access_token=8049d55a8049d55a8049d55a1480257774880498049d55add231156e76fd89a2f9f364e&v=5.120"\
                    .format(short_name)
    resp = requests.get(url=url_check)
    data = resp.json()
    return data.get('response')[0]['id']
