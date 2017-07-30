import re
import requests
import time
import youtube_dl

from PIL import Image
from google.cloud import vision
from io import BytesIO


def get_page_source(url):
    r = requests.get(url)
    return str(r.content)

def get_mosaics(page_content):
    match = (re.search('\"storyboard_spec\":\"([^\"]*)\"', page_content)
            .group(1).replace('\\\\', ''))
    sighs = re.findall('\$M#([^\|$]+)(?:\||$)', match)
    base_url = match[:match.find('|')] + '?sigh=$S'

    l_value = len(sighs)
    sigh = sighs[-1]
    m_value = 0

    base_url = base_url.replace('$L', str(l_value)).replace('$S', sigh)

    # get all mosaics
    imgs = {}
    img_keys = []
    while True:
        mosaic_url = base_url.replace('$N', 'M{}'.format(m_value))
        img_keys.append('L{}_M{}_{}'.format(l_value, m_value, sigh))

        r = requests.get(mosaic_url, stream=True)
        if r.status_code != 200:
            print('failed on img_key={}, so we\'re done'.format(img_keys[-1]))
            img_keys.pop()
            break

        r.raw.decode_content = True
        imgs[img_keys[-1]] = Image.open(r.raw)

        time.sleep(0.5) # do not set off youtube's firewall
        m_value += 1

    return img_keys, imgs, l_value

def get_vid_length(page_content):
    return int(re.search(
        '\"length\_seconds\":\"([0-9]*)\"',
        page_content).group(1))

def get_frame_interval(vid_length):
    if 15 <= vid_length < 120: return 1
    elif 120 <= vid_length < 300: return 2
    elif 300 <= vid_length < 900: return 5
    else: return 10

def get_frame_dims(mosaic_w, mosaic_h, num_full_rows, num_last_row, shape):
    if num_full_rows == 0:
        frame_width = mosaic_w // num_last_row
    else:
        frame_width = mosaic_w // shape

    if num_full_rows >= shape:
        frame_height = mosaic_h // shape
    else:
        frame_height = mosaic_h // num_full_rows

    return frame_width, frame_height

def get_timestamped_frames(img_keys, imgs, level, vid_length, progress_cb, so_far, task_weight):
    level_to_mosaic_shape = {1: 10, 2: 5, 3: 9, 4: 3}
    shape = level_to_mosaic_shape[level] # each mosaic has shape x shape frames
    frame_interval = get_frame_interval(vid_length)
    num_frames = (vid_length / frame_interval) + 2 # 1st & last frame always in

    num_full_rows = int(num_frames // shape)
    num_last_row = round((num_frames / shape - num_full_rows) * shape)

    frame_width, frame_height = get_frame_dims(
            imgs[img_keys[0]].size[0], imgs[img_keys[0]].size[1],
            num_full_rows, num_last_row, shape)

    timestamp = 0
    frames = {}

    for row_idx in range(num_full_rows):
        for col_idx in range(shape):
            # determine what img we're looking at
            global_frame_idx = row_idx * shape + col_idx
            img_idx = (global_frame_idx // (shape * shape))
            curr_img = imgs[img_keys[img_idx]]
            curr_img_row = round(((row_idx / shape) % 1) * shape)

            # crop and add to list with incrementing timestamp
            x = col_idx * frame_width
            y = curr_img_row * frame_height
            frames[timestamp] = (curr_img.crop((x, y, x+frame_width, y+frame_height)), img_keys[img_idx] + str(global_frame_idx))
            timestamp += frame_interval

            # update frontend progress bar
            progress_cb(so_far + (task_weight * (global_frame_idx / num_frames)), 100)
    return frames

def get_labels(frames, progress_cb, so_far, task_weight):
    client = vision.Client('treehacks-159123')
    new_frames = {}
    i = 0
    for timestamp, curr in frames.items():
        curr_img, img_key = curr
        img_bytes = BytesIO()
        curr_img.save(img_bytes, format='png')

        img = client.image(content=img_bytes.getvalue())
        labels = img.detect_labels()
        time.sleep(0.05) # don't set off the firewallll
        new_frames[timestamp] = (img_bytes.getvalue(), [l.description for l in labels], img_key)
        print ('{}/{}'.format(str(i), len(frames)), end='\r')
        i += 1
        progress_cb(so_far + ((i / len(frames.items())) * task_weight), 100)
    return new_frames

def get_video_deets(page_content, url):
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        res = ydl.extract_info(url, download=False)
        thumbnail_url = res['thumbnails'][0]['url']
        username = res['uploader_id']
        title = res['title']
        desc = res['description']
        vid_length = get_vid_length(page_content)
        return (title, username, desc, thumbnail_url, vid_length)

def get_labels_from_url(url, progress_cb, so_far, task_weight):
    page_content = get_page_source(url)
    deets = get_video_deets(page_content, url)
    progress_cb(1, 100) # get progress bar started
    so_far += 1
    frames = get_timestamped_frames(
            *get_mosaics(page_content),
            deets[-1], # vid_length
            progress_cb, so_far, 5) # 5 percent to get mosaics
    so_far += 5
    return get_labels(frames, progress_cb, so_far, task_weight), deets

