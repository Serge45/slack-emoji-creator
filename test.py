import slack_emoji_creator
from slack_emoji_creator import image_slice

if __name__ == '__main__':
    image_slice.gif_slice('1.gif', window_size=(80, 80), output_size=(64, 64), output_prefix='qq', skip_rate=1)
