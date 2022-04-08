#!/usr/bin/env python

import requests
import json
from bs4 import BeautifulSoup

# URLs
youtube_search_base = 'https://www.youtube.com/results?search_query=cute+'
youtube_video_url = 'https://www.youtube.com/watch?v='
giphy_search_base = 'https://giphy.com/search/cute-'


# Other
vid_list_raw = []
vid_list = []
vid_dict={}
gif_list=[]


def getVideo(animal):
    search_url = f'{youtube_search_base}{animal}&sp=EgIQAQ%253D%253D'
    search_results = requests.get(search_url)
    search_results_html = BeautifulSoup(search_results.text, 'html.parser')
    print(f"\n{search_url}\n\n")
    parsed_results = search_results_html.text.split('ytInitialData = ',1)[1].split(';if',1)[0]
    parsed_results_json = json.loads(parsed_results)
    vid_list_raw = parsed_results_json['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    for v in vid_list_raw:
        try:
            v_id = v.get('videoRenderer').get('videoId')
            v_link = f'{youtube_video_url}{v_id}'
            v_text = v.get('videoRenderer').get('title').get('runs')[0].get('text')
            v_thumbnail = v.get('videoRenderer').get('thumbnail').get('thumbnails')[0].get('url')
        except:
            pass
        vid_dict[v_link] = v_thumbnail
    link, thumbnail = random.choice(list(vid_dict.items()))
    return link, thumbnail

def getGif(animal):    
    search_url = f'{giphy_search_base}{animal}'
    search_results = requests.get(search_url)
    search_results_html = str(BeautifulSoup(search_results.text, 'html.parser'))
    search_results_html_parsed = search_results_html.split("Giphy.renderSearch(document.getElementById('react-target'), {\n",1)[1].split('gifs:',1)[1]
    results_json = search_results_html_parsed.split(',\n',1)[0]
    next_page = search_results_html_parsed.split(',\n',1)[1].split('nextUrl: "',1)[1].split('",',1)[0]
    for g in json.loads(results_json):
        gif_list.append(g.get('url'))
    link = random.choice(list(gif_list))
    gif_id = link.split('-')[-1]
    giphy_gif_url = f'https://media.giphy.com/media/{gif_id}/giphy.gif'
    return giphy_gif_url
