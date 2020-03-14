from os import path
import PIL
from PIL import Image, ImageSequence

SLACK_EMOJI_SIZE = (128, 128)

def _get_next_slice(image, window_size):
    w, h = image.size
    num_slice_x = w//window_size[0]
    num_slice_y = h//window_size[1]

    for j in range(num_slice_y):
        for i in range(num_slice_x):
            bounds = (i*window_size[0], j*window_size[1], (i+1)*window_size[0], (j+1)*window_size[1])
            yield image.crop(bounds)

def gif_slice(filepath, 
              output_prefix=None, 
              window_size=SLACK_EMOJI_SIZE, 
              output_size=SLACK_EMOJI_SIZE,
              skip_rate=1):
    if output_prefix is None or len(output_prefix) == 0:
        output_prefix = path.splitext(filepath)[0]

    ext_name = path.splitext(filepath)[1]

    assert ext_name.lower() == '.gif'
    assert type(skip_rate) is int
    assert skip_rate >= 1

    with Image.open(filepath) as im:
        w, h = im.size
        d = im.info['duration']
        num_slice_x = w//window_size[0]
        num_slice_y = h//window_size[1]

        slices = [[] for _ in range(num_slice_y*num_slice_x)]

        for frame in ImageSequence.Iterator(im):
            for i, img in enumerate(_get_next_slice(frame, window_size)):
                slices[i].append(img.resize(output_size))

        for i, s in enumerate(slices):
            s[0].save(f'{output_prefix}_{i}{ext_name}', format='GIF', append_images=s[1:-1:skip_rate], save_all=True, optimize=True, duration=d*skip_rate)
