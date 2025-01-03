from video_utils import *
from tracker_3 import *

def main():
    frames = read_video("traffic_video.mp4")

    track = Tracker()
    result = track.process_video(frames)

if __name__ == '__main__':
    main()