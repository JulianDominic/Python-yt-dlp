import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from helpers import Start, Download, set_download_location

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./yt-dlp.ui", self)
        self.setWindowIcon(QIcon("./transparent.ico"))
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
        self.start_button.clicked.connect(self.start_button_click)
        self.video_button.clicked.connect(self.video_button_click)
        self.audio_button.clicked.connect(self.audio_button_click)
    

    def start_button_click(self):
        self.video_button.setEnabled(False)
        self.audio_button.setEnabled(False)
        self.download_button.setEnabled(False)
        start = Start()
        self.video_link = self.input_url_field.text()
        if start.is_url(self.video_link):
            if start.is_youtube_url(self.video_link):
                self.video_button.setEnabled(True)
                self.audio_button.setEnabled(True)
                self.generate_download_options(self.video_link)
            else:
                self.download_button.setEnabled(True)

    
    def video_button_click(self):
        if not(self.audio_button.isEnabled()):
            self.audio_button.setEnabled(True)
            self.reset_hlayouts(self.button_hlayouts)
        self.video_button.setEnabled(False)
        

    def audio_button_click(self):
        self.reset_hlayouts(self.button_hlayouts)
        if not(self.video_button.isEnabled()):
            self.video_button.setEnabled(True)
        self.audio_button.setEnabled(False)

    
    def download_button_click(self):
        ...


    def generate_download_options(self, url):
        dl = Download()
        all_download_options, available_acodecs = dl.parse_video_information_dict(self.video_link)
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
        resolution_buttons = self.create_buttons_from_list_to_hlayout([str(res) for res in processed_download_options], self.resolution_hlayout)
        # print(resolution_buttons)
        acodec_buttons = self.create_buttons_from_list_to_hlayout(available_acodecs, self.vaudio_codec_hlayout)
    

    def create_buttons_from_list_to_hlayout(self, button_list:str, hlayout:QHBoxLayout) -> dict:
        hlayout_button_dict = {}
        for button in button_list:
            new_button = QPushButton(button, self)
            hlayout_button_dict[button] = new_button
            hlayout.addWidget(new_button)
        return hlayout_button_dict
    

    def resolution_button_click(self):
        ...

    
    def fps_button_click(self):
        ...

    
    def video_extension_button_click(self):
        ...


    def video_codec_button_click(self):
        ...

    
    def vaudio_codec_button_click(self):
        ...

    
    def audio_extension_button_click(self):
        ...

    
    def audio_codec_button_click(self):
        ...


    def reset_hlayouts(self, hlayouts:list):
        for hlayout in hlayouts:
            hlayout:QHBoxLayout
            while hlayout.count() > 0:
                button = hlayout.takeAt(0)
                widget = button.widget()
                if widget is not None:
                    widget.deleteLater()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing Window")
