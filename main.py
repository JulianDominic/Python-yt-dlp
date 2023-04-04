from yt_dlp import YoutubeDL
import re, os, sys
from dotenv import load_dotenv
from helpers import get_info, get_options, check_if_playlist, get_individual_links_from_playlist, clear_screen


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
    
    # Detect if it is a playlist
    is_playlist = check_if_playlist(URL)

    if is_playlist:
        links = get_individual_links_from_playlist(URL)
        for link in links:
            download_video(link)
    else:
        download_video(URL)


def set_download_location():
    load_dotenv()
    # Place the absolute path in the ".env" file
    download_path = os.getenv("download_path")
    os.chdir(download_path)


def get_user_options(res_options, aexts, title):
    clear_screen()
    print(f"Video being downloaded: {title}")
    if not(res_options):
        print("Sorry there's no information available!")
        sys.exit()
    
    while True:
        print([resolution for resolution in res_options])
        try:
            res = int(input("Choose your resolution\n> "))
            if res not in res_options:
                print("Invalid input\n")
                continue
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
            continue

        print(aexts)
        aext = input("Choose your audio extension\n> ")
        if aext not in aexts:
            print("Invalid input\n")
            continue
        break
    return res, vext, fps, aext


def download_video(video_link):
    res_set, vext_set, aexts, video_set, title = get_info(URL=video_link)
    res_options = get_options(res_set=res_set, vext_set=vext_set, video_set=video_set)
    res, vext, fps, aext =  get_user_options(res_options, aexts, title)

    # See help(YoutubeDL) for a list of available options and public functions
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
