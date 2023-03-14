from yt_dlp import YoutubeDL
import os
from dotenv import load_dotenv
from helpers import get_info, get_options
import re

def main():
    load_dotenv()
    download_path = os.getenv("download_path")
    os.chdir(download_path)

    url_regex = re.compile(
            r"^https?://"  # match http:// or https://
            r"([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}"  # match domain name
            r"(:[0-9]{1,5})?"  # optional port number
            r"(/.*)?$",  # match path and query string if present
            re.IGNORECASE
            )
    valid_url = False
    while not(valid_url):
        URL = input("Enter the link to the video\n> ")
        match = url_regex.search(URL)
        if match:
            valid_url = True
        else:
            print("Invalid URL.\n")
            continue

    res_set, vext_set, aexts, video_set = get_info(URL=URL)
    res_options = get_options(res_set=res_set, vext_set=vext_set, video_set=video_set)
    while True:
        print([resolution for resolution in res_options])
        try:
            res = int(input("Choose your resolution\n> "))
            if res not in res_options:
                print("Invalid input\n")
                continue
        except ValueError:
            print("Invalid input\n")
            continue

        print([vext for vext in res_options[res]])
        vext = input("Choose your video extension\n> ")
        if vext not in res_options[res]:
            print("Invalid input\n")
            continue

        print([fps for fps in res_options[res][vext]])
        try:
            fps = int(input("Choose your video fps\n> "))
            if fps not in res_options[res][vext]:
                print("Invalid input\n")
                continue
        except ValueError:
            print("Invalid input\n")
            continue

        print(aexts)
        aext = input("Choose your audio extension\n> ")
        if aext not in aexts:
            print("Invalid input\n")
            continue
        break

    #= See help(YoutubeDL) for a list of available options and public functions
    ydl_opts = {
        'format': f'bestvideo[height<={res}][fps={fps}]+bestaudio[ext={aext}]',
        'merge_output_format': f'{vext}'
        }

    # Send the URL and options selected into downloading
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)


if __name__ == "__main__":
    main()
