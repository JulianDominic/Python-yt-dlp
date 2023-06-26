#! python3
# main.py - This program allows users to download Youtube Videos via the CLI

from helpers import Start, Download, set_download_location


def main():
    start = Start()
    url = start.get_url_from_user()
    best = start.is_best()
    dl = Download()
    dl.download_video(url, best)

if __name__ == "__main__":
    set_download_location()
    main()
