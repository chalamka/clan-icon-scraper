from urllib.request import urlretrieve
from requests import get
from time import sleep

def format_download_url(base, clan_id):
    return base.format(clan_id[-3:], clan_id)


def download_icon_from_url(url, filename):
    img = urlretrieve(url, filename)


def get_clan_tag(url, clan_id, api_key):
    response = get(url, params={'clan_id': clan_id, 'application_id': api_key})
    parsed_response = response.json()
    clan_tag = None

    if parsed_response['status'] == 'ok':
        try:
            clan_tag = parsed_response['data'][clan_id]['tag']
            print("Found tag: {} for clan_id: {}".format(clan_tag, clan_id))
        except TypeError:
            print("Couldn't get a clan tag for id: {}".format(clan_id))
    else:
        print("API returned error: {} for clan_id: {}".format(parsed_response['error']['message'], clan_id))

    sleep(0.1)
    return clan_tag


def main():
    with open("config.txt") as fp:
        api_key = fp.readline().rstrip() 

    base_url = "http://na.wargaming.net/clans/media/clans/emblems/cl_{}/{}/emblem_32x32.png"
    api_url = "https://api.worldoftanks.com/wot/globalmap/claninfo/" 

    for clan_id in ['1000001505', '1000012800', 'bad_id', '10000128000']:
        clan_tag = get_clan_tag(api_url, clan_id, api_key)
        if clan_tag:
            filename = "icons/{}.jpg".format(clan_tag)
            url = format_download_url(base_url, clan_id)
            download_icon_from_url(url, filename)

if __name__ == '__main__':
    main()
