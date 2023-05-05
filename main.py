#! python3
# main.py - This program allows users to download Youtube Videos via the CLI

from yt_dlp import YoutubeDL
import re, os, sys
from dotenv import load_dotenv
from helpers import get_info, get_options, check_if_playlist, check_if_short, get_individual_links_from_playlist, clear_screen, extract_video_information, get_user_options


def main():
    set_download_location()

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

    yt_urls = ["youtube", "youtu.be"]
    if any(yt_url in URL for yt_url in yt_urls):
        info_result = extract_video_information(URL)
        # Detect if it is a playlist
        is_playlist = check_if_playlist(info_result)
        is_short = check_if_short(info_result)

        if is_playlist:
            links = get_individual_links_from_playlist(info_result)
            for link in links:
                info_result = extract_video_information(link)
                is_short = check_if_short(info_result)
                download_video(URL, best=False, info_result=info_result, yt_short=is_short)
        else:
            while True:
                user_choice_best = input("Skip selection to download best option? (Y/n): ")
                if user_choice_best.lower() == "n":
                    break
                elif user_choice_best.upper() == "Y":
                    clear_screen()
                    download_video(URL, best=True, info_result=info_result)
                    sys.exit()
                else:
                    print("Invalid input\n")
                    continue
            download_video(URL, best=False, info_result=info_result, yt_short=is_short)
            sys.exit()
    else:
        clear_screen()
        download_video(URL, best=True)


def set_download_location():
    load_dotenv()
    # Place the absolute path in the .env file
    download_path = os.getenv("download_path")
    os.chdir(download_path)


def download_video(video_link:str, best:bool, info_result:dict=None, yt_short:bool=None):
    if best:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s'
            }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_link)
            sys.exit()
    if info_result == None:
        info_result = extract_video_information(video_link)
    res_set, vext_set, aexts, video_set, title = get_info(info=info_result)
    res_options = get_options(res_set=res_set, vext_set=vext_set, video_set=video_set)
    res, vext, fps, aext =  get_user_options(res_options, aexts, title)
    clear_screen()

    # See help(YoutubeDL) for a list of available options and public functions
    if yt_short:
        ydl_opts = {
            'format': f'bestvideo[width<={res}][fps={fps}]+bestaudio[ext={aext}]',
            'merge_output_format': f'{vext}',
            'outtmpl': '%(title)s.%(ext)s'
            }
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={res}][fps={fps}]+bestaudio[ext={aext}]',
            'merge_output_format': f'{vext}',
            'outtmpl': '%(title)s.%(ext)s'
            }
    # Send the URL and options selected into downloading
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_link)


if __name__ == "__main__":
    main()
