import os, re, sys
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

class Start:
    def __init__(self):
        self.yt_playlist = False


    def get_url_from_user(self) -> str:
        """
        Prompts the user for the video link
        """
        valid = False
        while not(valid):
            video_link = input("Enter the video link for download \n> ")
            valid = self.is_url(video_link)
            clear_screen()
        else:
            return video_link
        
    
    def video_or_audio(self) -> bool:
        """
        Prompts the user to choose between downloading a video file or an audio file. Output: 1 True, 2 False
        """
        while True:
            user_input = input("Do you want to download the video or just the audio?\n[1] Video\n[2] Audio\n> ")
            if user_input not in ["1", "2"]:
                print("Please enter either '1' or '2'.")
            else:
                if user_input == "1":
                    clear_screen()
                    return True
                elif user_input == "2":
                    clear_screen()
                    return False


    def is_url(self, url:str) -> bool:
        """
        Checks if the input is a URL
        """
        url_regex = re.compile(
                r"^https?://"  # match http:// or https://
                r"([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}"  # match domain name
                r"(:[0-9]{1,5})?"  # optional port number
                r"(/.*)?$",  # match path and query string if present
                re.IGNORECASE
                )
        return url_regex.search(url)
    

    def is_best(self, url:str) -> bool:
        """
        Checks if the user has chosen the 'best' option for ydl_opts
        """
        # Since the custom download options only works for Youtube Videos,
        # other links will be passed through with the 'best' option
        if not(self.is_youtube_url(url)):
            return True
        while True:
            user_best = input("Skip custom settings and download the recommended settings? (Y/n): ").lower()
            if user_best == "y" or user_best == "":
                clear_screen()
                return True
            elif user_best == "n":
                clear_screen()
                return False
    

    def is_youtube_url(self, url:str) -> bool:
        """
        Checks if the URL is for a youtube video
        """
        yt_urls = ["youtube", "youtu.be"]
        if any([yt_url in url for yt_url in yt_urls]):
            self.is_youtube_playlist(url)
            return True
        else:
            return False
        
    
    def is_youtube_playlist(self, url:str) -> None:
        """
        Checks if the URL is for a youtube playlist
        """
        if "playlist" in url:
            self.yt_playlist = True
        else:
            self.yt_playlist = False
        return None
        
    
    def is_instagram_url(self, url:str) -> bool:
        """
        Checks if the URL is from Instagram
        """
        insta_urls = ["instagram"]
        if any([insta_url in url for insta_url in insta_urls]):
            return True
        else:
            return False
        

    def is_twitter_url(self, url:str) -> bool:
        """
        Checks if the URL is from Twitter (or X)
        """
        twitter_urls = ["twitter", "t.co"]
        if any([twitter_url in url for twitter_url in twitter_urls]):
            return True
        else:
            return False


class Download:
    def extract_video_information_dict(self, video_link:str, ydl_opts=None) -> dict:
        """
        Gets the video information provided by the website
        """
        original_stdout = stop_stdout()
        if ydl_opts is None:
            with YoutubeDL() as ydl:
                info_result = ydl.extract_info(video_link, download=False)
        else:
            with YoutubeDL(ydl_opts) as ydl:
                info_result = ydl.extract_info(video_link, download=False)
        start_stdout(original_stdout)
        return info_result
    

    def process_playlist(self, video_link:str) -> list[str]:
        """
        Gets the URLs of the videos that are available in the playlist
        """
        ydl_opts = {
            'extract_flat': 'discard_in_playlist',
            'fragment_retries': 10,
            'ignoreerrors': 'only_download',
            'postprocessors': [{'key': 'FFmpegConcat',
                                'only_multi_video': True,
                                'when': 'playlist'}],
            'retries': 10
        }
        print("Processing the playlist...")
        playlist_dict = self.extract_video_information_dict(video_link, ydl_opts)
        print("Finished processing the playlist.")
        return [video_dict['url'] for video_dict in playlist_dict['entries'] if video_dict != None]
    

    def get_available_acodecs(self, all_formats:list) -> list[set]:
        """
        Get the available audio codecs
        """
        available_acodecs = set()
        for single_format in all_formats:
            single_format:dict
            acodec = single_format.get("acodec")
            if acodec is None or acodec == "none" or acodec == "video only" or acodec == "unknown":
                continue
            else:
                acodec:str
                available_acodecs.add(acodec.split('.')[0])
        return sorted(available_acodecs)


    def parse_video_information_dict(self, video_link:str) -> list[list]:
        """
        Parses the video_information_dict to get the download options
        """
        video_information_dict = self.extract_video_information_dict(video_link)
        all_formats = video_information_dict["formats"]
        
        all_download_options = []
        for single_format in all_formats:
            download_options = {
                "resolution": None,
                "fps": None,
                "video_ext": None,
                "vcodec": None,
                "aspect_ratio": None
                }
            try:
                # Using the 'resolution' key instead of 'format_note' because resolution is essentially <width>x<height>
                # Thus, it would be easier to get the relevant information more easily to pass into ydl_opts
                resolution: str = single_format["resolution"]
                fps: str = single_format["fps"]
                video_ext: str = single_format["ext"]
                vcodec: str = "".join(single_format["vcodec"][0:4])
                aspect_ratio: float = single_format["aspect_ratio"]

                if resolution[0].isdigit() and vcodec != 'none':
                    # 3gp has been causing some issues | TODO: Possibly fix this
                    if video_ext == '3gp':
                        continue

                    resolution = min([int(res) for res in resolution.split('x')])

                    download_options["resolution"] = resolution
                    download_options["fps"] = int(fps)
                    download_options["video_ext"] = video_ext
                    download_options["vcodec"] = vcodec
                    download_options["aspect_ratio"] = aspect_ratio

                    all_download_options.append(download_options)

            except KeyError:
                continue

        else:
            clear_screen()
            available_acodecs = self.get_available_acodecs(all_formats)
            return [all_download_options, available_acodecs]
    

    def get_user_download_video_options(self, video_link:str) -> list:
        """
        Get the user's input & download option
        """
        all_download_options, available_acodecs = self.parse_video_information_dict(video_link)
        processed_download_options = {}
        for download_option in all_download_options:
            resolution = download_option["resolution"]
            fps = download_option["fps"]
            video_ext = download_option["video_ext"]
            vcodec = download_option["vcodec"]
            aspect_ratio = download_option["aspect_ratio"]
            
            resolution = int(resolution)
            if not(resolution in processed_download_options):
                processed_download_options[resolution] = {}
            if not(fps in processed_download_options[resolution]):
                processed_download_options[resolution][fps] = {}
            if not(video_ext in processed_download_options[resolution][fps]):
                processed_download_options[resolution][fps][video_ext] = []
            if not(vcodec in processed_download_options[resolution][fps][video_ext]):
                processed_download_options[resolution][fps][video_ext] += [vcodec]
        
        flag_resolution = False
        flag_fps = False
        flag_video_ext = False
        flag_vcodec = False
        flag_acodec = False

        while not(flag_resolution):
            print([i for i in processed_download_options])
            try:
                user_resolution = int(input("Choose your resolution\n> "))
                if user_resolution not in processed_download_options:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                flag_resolution = True
        
        while not(flag_fps):
            print([j for j in processed_download_options[user_resolution]])
            try:
                user_fps = int(input("Choose your video FPS\n> "))
                if user_fps not in processed_download_options[user_resolution]:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                flag_fps = True

        while not(flag_video_ext):
            print([k for k in processed_download_options[user_resolution][user_fps]])
            try:
                user_video_ext = input("Choose your video extension\n> ")
                if user_video_ext not in processed_download_options[user_resolution][user_fps]:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                flag_video_ext = True

        while not(flag_vcodec):
            print(processed_download_options[user_resolution][user_fps][user_video_ext])
            try:
                user_vcodec = input("Choose your video codec\n> ")
                if user_vcodec not in processed_download_options[user_resolution][user_fps][user_video_ext]:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                flag_vcodec = True
        
        while not(flag_acodec):
            print([l for l in available_acodecs])
            try:
                user_acodec = input("Choose your audio codec\n> ")
                if user_acodec not in available_acodecs:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                flag_acodec = True

        clear_screen()
        return [user_resolution, user_fps, user_video_ext, user_vcodec, user_acodec, aspect_ratio]
    

    def download_subtitles(self, ydl_opts:dict):
        """
        Asks the user whether they want to download subtitles provided by the creator. English only.
        """
        subtitle_decision = input("Download English subs? (Y/n): ")
        if subtitle_decision.lower() in ['y', '']:
            ydl_opts['subtitleslangs'] = ['en.*']
            ydl_opts['writeautomaticsub'] =  False
            ydl_opts['writesubtitles'] = True
        return ydl_opts
    

    def download_video(self, video_link:str, best=False, user_resolution=None, user_fps=None, user_video_ext=None, user_vcodec=None, user_acodec=None, aspect_ratio=None) -> None:
        """
        Sends the download options into the YoutubeDL class's download() method
        """
        if best:
            url_checker = Start()
            ydl_opts = {
                'ignoreerrors': 'only_download',
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s'
                }
            if url_checker.is_instagram_url(video_link) or url_checker.is_twitter_url(video_link):
                user_browser = input("Enter the name of the browser you use to access the link (eg. Chrome, Firefox)\n> ")
                ydl_opts['cookiesfrombrowser'] = [user_browser.lower()]
        else:
            user_resolution, user_fps, user_video_ext, user_vcodec, user_acodec, aspect_ratio = self.get_user_download_video_options(video_link)

            # There are vertical videos that are not shorts; Hence the video_duration is not a requirement
            if aspect_ratio < 1:
                ydl_opts = {
                    'format': f'bestvideo[width<={user_resolution}][fps={user_fps}][vcodec^={user_vcodec}]+bestaudio[acodec^={user_acodec}]',
                    'merge_output_format': f'{user_video_ext}',
                    'outtmpl': '%(title)s.%(ext)s'
                    }
            else:
                ydl_opts = {
                    'format': f'bestvideo[height<={user_resolution}][fps={user_fps}][vcodec^={user_vcodec}]+bestaudio[acodec^={user_acodec}]',
                    'merge_output_format': f'{user_video_ext}',
                    'outtmpl': '%(title)s.%(ext)s',
                    }
            ydl_opts = self.download_subtitles(ydl_opts)
        # Send the URL and options selected into downloading
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_link)
        return None
    

    def get_user_audio_options(self, video_link:str) -> str:
        """
        Get the user's prefered audio options. (i) ext (ii) codec
        """
        video_information_dict = self.extract_video_information_dict(video_link)
        all_formats = video_information_dict["formats"]
        acodecs = self.get_available_acodecs(all_formats)
        
        while True:
            audio_exts = ["m4a","aac","mp3","ogg","opus","webm"]
            print([audio_ext for audio_ext in audio_exts])
            try:
                user_audio_ext = input("Choose your audio extension\n> ")
                if user_audio_ext not in audio_exts:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                break

        while True:
            print([acodec for acodec in acodecs])
            try:
                user_audio_codec = input("Choose your audio codec\n> ")
                if user_audio_codec not in acodecs:
                    print("Invalid input\n")
                    continue
            except Exception as e:
                print(e)
                continue
            else:
                return [user_audio_ext, user_audio_codec]


    def download_audio(self, video_link:str, audio_ext=None, acodec=None) -> None:
        """
        Download the best audio for the user using YoutubeDL class's download() method
        """
        user_audio_options = self.get_user_audio_options(video_link)
        audio_ext, acodec = user_audio_options[0], user_audio_options[1]
        ydl_opts = {
            'format': f'bestaudio[acodec^={acodec}]',
            'outtmpl': '%(title)s.' + audio_ext
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_link)
        return None


def clear_screen() -> None:
    """
    Clear the console screen
    """
    os.system('cls' if os.name=='nt' else 'clear')
    return None


def set_download_location() -> None:
    """
    Sets the download location of the video file by changing the working directory to the download location
    """
    load_dotenv()
    # Place the absolute path in the .env file
    download_path = os.getenv("download_path")
    os.chdir(download_path)
    return None


def stop_stdout() -> sys.stdout:
    """
    Stops the standard output
    """
    original_stdout = sys.stdout
    sys.stdout = open('NUL', 'w')
    return original_stdout


def start_stdout(original_stdout:sys.stdout) -> None:
    """
    Starts the standard output
    """
    sys.stdout = original_stdout
    return None
