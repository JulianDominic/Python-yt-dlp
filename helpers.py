import os, re
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

class Start:
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

    def is_url(self, url: str) -> bool:
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
        if url_regex.search(url):
            return True
        return False
    

    def is_best(self) -> bool:
        """
        Checks if the user has chosen the 'best' option
        """
        while True:
            user_best = input("Skip custom settings and download the recommended settings? (Y/n): ").lower()
            if user_best == "y" or user_best == "":
                clear_screen()
                return True
            elif user_best == "n":
                clear_screen()
                return False


class Download:
    def extract_video_information_dict(self, video_link:str) -> dict:
        """
        Gets the video information provided by the website
        """
        with YoutubeDL() as ydl:
            info_result = ydl.extract_info(video_link, download=False)
        return info_result
    

    def parse_video_information_dict(self, video_link:str) -> list:
        """
        Parses the video_information_dict to get the download options
        """
        video_information_dict = self.extract_video_information_dict(video_link)
        video_duration = video_information_dict["duration"]
        all_formats = video_information_dict["formats"]
        
        all_download_options = []
        for single_format in all_formats:
            download_options = {
                "resolution": None,
                "fps": None,
                "video_ext": None
                }
            try:
                format_note: str = single_format["format_note"]
                fps: str = single_format["fps"]
                video_ext: str = single_format["ext"]
                if format_note[0].isdigit():
                    resolution = format_note.split('p')[0]
                    download_options["resolution"], download_options["fps"], download_options["video_ext"] = resolution, fps, video_ext
                    all_download_options.append(download_options)
            except KeyError:
                continue
        else:
            clear_screen()
            return [video_duration, all_download_options]
    

    def get_user_download_options(self, video_link:str) -> list:
        """
        Get the user's input & download option
        """
        video_duration, all_download_options = self.parse_video_information_dict(video_link)
        processed_download_options = {}
        for download_option in all_download_options:
            resolution, fps, video_ext = download_option["resolution"], download_option["fps"], download_option["video_ext"]
            resolution = int(resolution)
            if not(resolution in processed_download_options):
                processed_download_options[resolution] = {}
            if not(fps in processed_download_options[resolution]):
                processed_download_options[resolution][fps] = []
            if not(video_ext in processed_download_options[resolution][fps]):
                processed_download_options[resolution][fps] += [video_ext]
        
        flag_resolution = False
        flag_fps = False
        flag_video_ext = False

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
            print(processed_download_options[user_resolution][user_fps])
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
        clear_screen()
        return [video_duration, user_resolution, user_fps, user_video_ext]
    

    def download_video(self, video_link, best=False) -> None:
        """
        Sends the download options into the YoutubeDL function
        """
        if best:
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s'
                }
        else:
            video_duration, user_resolution, user_fps, user_video_ext = self.get_user_download_options(video_link)
            if video_duration <= 60:
                ydl_opts = {
                    'format': f'bestvideo[width<={user_resolution}][fps={user_fps}]+bestaudio',
                    'merge_output_format': f'{user_video_ext}',
                    'outtmpl': '%(title)s.%(ext)s'
                    }
            else:
                ydl_opts = {
                    'format': f'bestvideo[height<={user_resolution}][fps={user_fps}]+bestaudio',
                    'merge_output_format': f'{user_video_ext}',
                    'outtmpl': '%(title)s.%(ext)s'
                    }
        # Send the URL and options selected into downloading
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
    load_dotenv()
    # Place the absolute path in the .env file
    download_path = os.getenv("download_path")
    os.chdir(download_path)
    return None