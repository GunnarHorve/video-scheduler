"""
Daily Scheduled YouTube videos
"""

import argparse
import logging
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
import schedule
import time

logging.basicConfig(
    filename='out.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger()
FRIENDLY_NAME = ""          # ex: "Living Room TV"

def fetch_cl_args():
    def discover_chromecasts():
        log.info("searching network for chromecasts")
        chromecasts, browser = pychromecast.discovery.discover_chromecasts()
        pychromecast.discovery.stop_discovery(browser)

        if len(chromecasts) == 0:
            log.critical("no chromecast-capable devices found.  Aborting program.")
            assert len(chromecasts) > 0, "There must be at least one chromecast-capable device in-network for this tool to function."
        else:
            log.info(f"detected {len(chromecasts)} chromecast-capable devices on your network")

        return chromecasts

    def assemble_cl_parser(chromecasts):
        parser = argparse.ArgumentParser(description='Schedule YouTube videos for headless streaming')
        parser.add_argument('-c', '--cast', required=True, help=f'Name of device to cast to. Choose one of {[cast[3] for cast in chromecasts]}')

        opts = parser.parse_args()
        FRIENDLY_NAME = opts.cast

    chromecasts = discover_chromecasts()
    assemble_cl_parser(chromecasts)


def play_youtube_video(video_id):
    log.info(f"casting {video_id} to {friendly_name}")

    # connect to device
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[FRIENDLY_NAME])
    cast = chromecasts[0]
    cast.wait()

    # play youtube video
    yt = YouTubeController()
    cast.register_handler(yt)
    yt.play_video(video_id)

    # Shut down discovery
    pychromecast.discovery.stop_discovery(browser)


def play_next_in_queue(consume=False):
    with open('./video-queue.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    if consume:
        with open('./video-queue.txt', 'w') as fout:
            fout.writelines(data[1:])

    play_youtube_video(data[0].rstrip())


def main():
    log.info("program startup")
    fetch_cl_args()
    schedule.every().day.at("07:55").do(play_next_in_queue, consume=False)
    schedule.every().day.at("08:45").do(play_next_in_queue, consume=True)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log.critical("KeyboardInterrupt detected.  Aborting program.")
        raise
