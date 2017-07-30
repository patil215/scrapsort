from app.utils import caption
from google.cloud import storage
from app.utils import vision
from algoliasearch import algoliasearch
from urllib import parse

client = algoliasearch.Client("Y9MCTNJ20T", "5c85dabf76ed1ba90c86b74f3470d965")
IMAGE_BUCKET= 'treehacks-img'

def merge(url, captions, frames, timestamps, progress_cb, so_far, task_weight):
    out = []
    total = len(timestamps)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(IMAGE_BUCKET)
    for i, time in enumerate(timestamps):
        data = {}
        if time in frames:
            blob = bucket.blob(frames[time][2] + '.png')
            blob.upload_from_string(frames[time][0])
            print(blob.public_url)
            data['labels'] = frames[time][1]
            data['image_url'] = blob.public_url
        if time in captions:
            data['text'] = captions[time]
        data['time'] = time * 1000
        data['url'] = url
        out.append(data)
        progress_cb(so_far + (task_weight * (i / total)), 100)
    return out

def tag_and_upload(url, progress_cb):
    # 70 percent
    frames, deets = vision.get_labels_from_url(url, progress_cb, 0, 70)

    # 20 percent
    timestamps = list(sorted(frames.keys()))
    captions = caption.get_timestamped_captions(url, timestamps, progress_cb, 70, 20)

    # 10 percent
    title, username, desc, thumbnail_url, vid_length = deets
    res = merge(url, captions, frames, timestamps, progress_cb, 90, 10)
    for r in res:
        r['title'] = title
        r['username'] = username
        r['desc'] = desc
        r['thumb'] = thumbnail_url
        r['vid_length'] = vid_length

    index = client.init_index("frames")
    index.add_objects(res)
    progress_cb(100, 100)
