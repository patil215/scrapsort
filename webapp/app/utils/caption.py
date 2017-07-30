from __future__ import unicode_literals
import youtube_dl
import requests
import os
from io import BytesIO, StringIO
from pycaption import WebVTTReader

def findMatches(captions):
    index = client.init_index("captions")
    arr = []
    for caption in captions:
        arr.append({'start':caption.start.ordinal, 'end': caption.end.ordinal, 'text': caption.text, 'video': url})
    index.add_objects(arr)

def dict_format(captions, timestamps, progress_cb, so_far, task_weight):
    out = {}
    diff = (timestamps[1] - timestamps[0])

    total = len(captions)
    for i, caption in enumerate(captions):
        caption_timestamp = caption.start / 1000000
        if diff * int(caption_timestamp / diff) not in out:
            out[diff * int(caption_timestamp / diff)] = caption.get_text()
        else:
            out[diff * int(caption_timestamp / diff)] += ' ' + caption.get_text()

        # update frontend progress bar
        progress_cb(so_far + (task_weight * i / total), so_far + total)
    return out

def getCaptions(url, progress_cb, so_far, task_weight):
    ydl = youtube_dl.YoutubeDL({'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True})
    with ydl:
        res = ydl.extract_info(url, download=False)
        if res['requested_subtitles'] and res['requested_subtitles']['en']:
            print ('Grabbing vtt file from ' + res['requested_subtitles']['en']['url'])
            response = requests.get(res['requested_subtitles']['en']['url'], stream=True)
            b = BytesIO()
            for block in response.iter_content(1024):
                b.write(block)
            b.seek(0)
            arr = WebVTTReader().read(b.read().decode('ascii'))
            progress_cb(so_far + task_weight, so_far + task_weight)
            return arr.get_captions('en-US')
        else:
            return []
            print ('Youtube Video does not have any english captions')
            return None

def get_timestamped_captions(url, timestamps, progress_cb, so_far, task_weight):
    captions = getCaptions(url, progress_cb, so_far, task_weight * 0.9) # 90 percent of this task
    return dict_format(captions, timestamps, progress_cb, so_far + task_weight * 0.9, task_weight * 0.1) # 10 percent


