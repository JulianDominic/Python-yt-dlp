import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from helpers import Start, Download, set_download_location
from dotenv import load_dotenv

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        load_dotenv()
        uic.loadUi(f"{os.getenv('ui_path')}", self)
        self.setWindowIcon(QIcon(f"{os.getenv('transparent_icon_path')}"))
        self.all_video_download_options = None
        self.available_acodecs = None
        self.extracted_yt_download_opts = []
        self.video_link = None
        self.button_hlayouts = \
        [
            self.resolution_hlayout,
            self.fps_hlayout,
            self.video_extension_hlayout,
            self.video_codec_hlayout,
            self.vaudio_codec_hlayout,
            self.audio_extension_hlayout,
            self.audio_codec_hlayout
        ]
        self.processed_download_options = {}
        self.resolution_buttons = None
        self.fps_buttons = None
        self.video_extension_buttons = None
        self.video_codec_buttons = None
        self.vaudio_codec_buttons = None
        self.user_video_download_options = {
            "resolution": None,
            "fps": None,
            "video_extension": None,
            "video_codec": None,
            "audio_codec": None
        }
        
        self.aspect_ratio = None
        self.audio_exts = ["m4a","aac","mp3","ogg","opus","webm"]
        self.audio_extension_buttons = None
        self.audio_codec_buttons = None
        self.user_audio_download_options = {
            "audio_extension": None,
            "audio_codec": None
        }

        self.download_type = None
        self.start_button.clicked.connect(self.start_button_click)
        self.video_button.clicked.connect(self.video_button_click)
        self.audio_button.clicked.connect(self.audio_button_click)
        self.download_button.clicked.connect(self.download_button_click)
        self.dl = Download()
    

    def start_button_click(self):
        self.update_output_download_option(fully_reset=True)
        self.reset_hlayouts(self.button_hlayouts)
        self.video_button.setEnabled(False)
        self.audio_button.setEnabled(False)
        self.download_button.setEnabled(False)
        start = Start()
        self.video_link = self.input_url_field.text()
        if start.is_url(self.video_link):
            if start.is_youtube_url(self.video_link):
                self.video_button.setEnabled(True)
                self.audio_button.setEnabled(True)
                self.all_video_download_options, self.available_acodecs = self.dl.parse_video_information_dict(self.video_link)
            else:
                self.download_button.setEnabled(True)

    
    def video_button_click(self):
        self.download_type = "video"
        if not(self.audio_button.isEnabled()):
            self.audio_button.setEnabled(True)
            self.reset_hlayouts(self.button_hlayouts)
        self.video_button.setEnabled(False)
        self.generate_video_download_options(self.all_video_download_options, self.available_acodecs)
        

    def audio_button_click(self):
        self.download_type = "audio"
        self.reset_hlayouts(self.button_hlayouts)
        if not(self.video_button.isEnabled()):
            self.video_button.setEnabled(True)
        self.audio_button.setEnabled(False)
        self.audio_extension_buttons = self.create_buttons_from_list_to_hlayout(self.audio_exts, self.audio_extension_hlayout, option="audio_extension")

    
    def download_button_click(self):
        if self.download_type == "video":
            user_resolution = self.user_video_download_options["resolution"]
            user_fps = self.user_video_download_options["fps"]
            user_video_ext = self.user_video_download_options["video_extension"]
            user_vcodec = self.user_video_download_options["video_codec"]
            user_acodec = self.user_video_download_options["audio_codec"]
            self.dl.download_video(self.video_link, gui=True, 
                                user_resolution=user_resolution,
                                user_fps=user_fps,
                                user_video_ext=user_video_ext,
                                user_vcodec=user_vcodec,
                                user_acodec=user_acodec,
                                aspect_ratio=self.aspect_ratio)
        elif self.download_type == "audio":
            audio_ext = self.user_audio_download_options["audio_extension"]
            acodec = self.user_audio_download_options["audio_codec"]
            self.dl.download_audio(self.video_link, gui=True,
                                   audio_ext=audio_ext,
                                   acodec=acodec)
        self.download_button.setEnabled(False)


    def generate_video_download_options(self, all_download_options, available_acodecs):
        self.processed_download_options = {}
        for download_option in all_download_options:
            resolution = download_option["resolution"]
            fps = download_option["fps"]
            video_ext = download_option["video_ext"]
            vcodec = download_option["vcodec"]
            self.aspect_ratio = download_option["aspect_ratio"]
            
            resolution = int(resolution)
            if not(resolution in self.processed_download_options):
                self.processed_download_options[resolution] = {}
            if not(fps in self.processed_download_options[resolution]):
                self.processed_download_options[resolution][fps] = {}
            if not(video_ext in self.processed_download_options[resolution][fps]):
                self.processed_download_options[resolution][fps][video_ext] = []
            if not(vcodec in self.processed_download_options[resolution][fps][video_ext]):
                self.processed_download_options[resolution][fps][video_ext] += [vcodec]
        
        self.resolution_buttons = self.create_buttons_from_list_to_hlayout([str(res) for res in self.processed_download_options], self.resolution_hlayout, option="resolution")
    

    def create_buttons_from_list_to_hlayout(self, button_list:str, hlayout:QHBoxLayout, option=None) -> dict:
        hlayout_button_dict = {}
        for button in button_list:
            new_button = QPushButton(button, self)
            hlayout_button_dict[new_button] = button
            hlayout.addWidget(new_button)
            if option == "resolution":
                new_button.clicked.connect(self.resolution_button_click)
            elif option == "fps":
                new_button.clicked.connect(self.fps_button_click)
            elif option == "video_extension":
                new_button.clicked.connect(self.video_extension_button_click)
            elif option == "video_codec":
                new_button.clicked.connect(self.video_codec_button_click)
            elif option == "vaudio_codec":
                new_button.clicked.connect(self.vaudio_codec_button_click)
            elif option == "audio_extension":
                new_button.clicked.connect(self.audio_extension_button_click)
            elif option == "audio_codec":
                new_button.clicked.connect(self.audio_codec_button_click)
        return hlayout_button_dict
    

    def resolution_button_click(self):
        self.reset_hlayouts([self.fps_hlayout, self.video_extension_hlayout, self.video_codec_hlayout, self.vaudio_codec_hlayout])
        self.reset_output_download_option("video", "resolution")
        clicked_button = self.sender()
        resolution = int(self.resolution_buttons[clicked_button])
        self.user_video_download_options["resolution"] = resolution
        self.update_output_download_option("video")

        fps_list = self.processed_download_options[resolution]
        self.fps_buttons = self.create_buttons_from_list_to_hlayout([str(fps) for fps in fps_list], self.fps_hlayout, option="fps")

    
    def fps_button_click(self):
        self.reset_hlayouts([self.video_extension_hlayout, self.video_codec_hlayout, self.vaudio_codec_hlayout])
        self.reset_output_download_option("video", "fps")
        clicked_button = self.sender()
        fps = int(self.fps_buttons[clicked_button])
        self.user_video_download_options["fps"] = fps
        self.update_output_download_option("video")

        video_extension_list = self.processed_download_options[self.user_video_download_options["resolution"]][fps]
        self.video_extension_buttons = self.create_buttons_from_list_to_hlayout([video_extension for video_extension in video_extension_list], self.video_extension_hlayout, option="video_extension")

    
    def video_extension_button_click(self):
        self.reset_hlayouts([self.video_codec_hlayout, self.vaudio_codec_hlayout])
        self.reset_output_download_option("video", "video_extension")
        clicked_button = self.sender()
        video_extension = self.video_extension_buttons[clicked_button]
        self.user_video_download_options["video_extension"] = video_extension
        self.update_output_download_option("video")

        video_codec_list = self.processed_download_options[self.user_video_download_options["resolution"]][self.user_video_download_options["fps"]][video_extension]
        self.video_codec_buttons = self.create_buttons_from_list_to_hlayout([video_codec for video_codec in video_codec_list], self.video_codec_hlayout, option="video_codec")


    def video_codec_button_click(self):
        self.reset_hlayout(self.vaudio_codec_hlayout)
        self.reset_output_download_option("video", "video_codec")
        clicked_button = self.sender()
        video_codec = self.video_codec_buttons[clicked_button]
        self.user_video_download_options["video_codec"] = video_codec
        self.update_output_download_option("video")

        self.vaudio_codec_buttons = self.create_buttons_from_list_to_hlayout(self.available_acodecs, self.vaudio_codec_hlayout, option="vaudio_codec")

    
    def vaudio_codec_button_click(self):
        clicked_button = self.sender()
        vaudio_codec = self.vaudio_codec_buttons[clicked_button]
        self.user_video_download_options["audio_codec"] = vaudio_codec
        self.update_output_download_option("video")
        self.download_button.setEnabled(True)

    
    def audio_extension_button_click(self):
        self.reset_hlayout(self.audio_codec_hlayout)
        self.reset_output_download_option("audio", "audio_extension")
        clicked_button = self.sender()
        audio_extension = self.audio_extension_buttons[clicked_button]
        self.user_audio_download_options["audio_extension"] = audio_extension
        self.update_output_download_option("audio")

        self.audio_codec_buttons = self.create_buttons_from_list_to_hlayout(self.available_acodecs, self.audio_codec_hlayout, option="audio_codec")

    
    def audio_codec_button_click(self):
        clicked_button = self.sender()
        audio_codec = self.audio_codec_buttons[clicked_button]
        self.user_audio_download_options["audio_codec"] = audio_codec
        self.update_output_download_option("audio")
        self.download_button.setEnabled(True)


    def reset_hlayouts(self, hlayouts:list):
        for hlayout in hlayouts:
            self.reset_hlayout(hlayout)
    

    def reset_hlayout(self, hlayout:QHBoxLayout):
        while hlayout.count() > 0:
            button = hlayout.takeAt(0)
            widget = button.widget()
            if widget is not None:
                widget.deleteLater()
    

    def reset_output_download_option(self, type, option):
        video_options = {"resolution": 0, "fps": 1, "video_extension": 2, "video_codec": 3, "audio_codec": 4}
        audio_options = {"audio_extension": 0, "audio_codec": 1}
        count = 0
        if type == "video":
            for k in self.user_video_download_options:
                if video_options[option] < count:
                    self.user_video_download_options[k] = None
                count += 1
        elif type == "audio":
            for k in self.user_audio_download_options:
                if audio_options[option] < count:
                    self.user_audio_download_options[k] = None
        self.download_button.setEnabled(False)
    

    def update_output_download_option(self, option=None, fully_reset=False):
        string = ""
        if fully_reset:
            self.output_download_options.setText(string)
        else:
            if option == "video":
                for settings, value in self.user_video_download_options.items():
                    string += f"{settings}: {value} "
            elif option == "audio":
                for settings, value in self.user_audio_download_options.items():
                    string += f"{settings}: {value} "
            self.output_download_options.setText(string)

# TODO: Add and figure out how to implement a proper progress bar. Current issue: Circular Importing.

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()
    set_download_location()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing Window")
