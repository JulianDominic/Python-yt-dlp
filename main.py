#! python3
# main.py - This program allows users to download Youtube Videos via the CLI

from helpers import Start, Download, set_download_location


def main():
    start = Start()
    url = start.get_url_from_user()
    video_audio = start.video_or_audio()
    dl = Download()
    if video_audio:
        best = start.is_best(url)
        dl.download_video(url, best)
    else:
        dl.download_audio(url)

if __name__ == "__main__":
    set_download_location()
    main()
