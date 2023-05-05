# Python-yt-dlp
*Has been tested on Win10/11 and Arch Linux*

This allows users to select their desired resolution, video extension, audio extension, and fps when downloading a video via the command line interface (CLI). 
Usage:
  1. Ensure that you have the [python-dotenv](https://pypi.org/project/python-dotenv/) and [yt-dlp](https://github.com/yt-dlp/yt-dlp#installation) modules installed. You do so by doing `pip install -r requirements.txt`. Essentially, download all the dependencies.
  2. As well as the [FFMPEG](https://ffmpeg.org/download.html) program to merge video/audio files.
  3. Create a `.env` file to store your `download_path` or you can manually add it into `main.py` directly.
  4. Run the script.

# For more detailed instructions:
# Prerequisites:
1. Download Python
2. Download 7zip
3. Download FFMPEG
4. Create a folder of where you want to download the videos
5. Download the files from Github
6. Create a .env file to store your download path

## (Step 1: Download Python):
1. Go to `https://www.python.org/downloads/release/python-3113/`
2. Scroll all the way to the bottom, and click on `Windows installer (64-bit)`
3. Run the file
4. ADD PYTHON TO PATH (THIS IS IMPORTANT; ESPECIALLY IF YOU WANT TO RUN THE SCRIPT VIA A BATCH FILE)
5. Keep pressing `Next`
6. If given an option, DISABLE PATH LENGTH LIMIT!!! 

## (Step 3: Download FFMPEG):
1. Go to `https://ffmpeg.org/download.html`
2. Click on the Windows logo
3. Click on `Windows Build from gyan.dev`; You will be redirected to another website
4. Click on `ffmpeg-git-essentials.7z`
5. Extract the file using 7zip
6. (a) Open the folder, open `bin`, copy/cut and paste the `ffmpeg.exe` into the download path (the folder where u want to download the videos in)
6. (b) You can add `ffmpeg.exe` to `PATH` instead of doing (a).

## (Step 5: Download the files from Github) & (Step 6: Create a .env file to store your download path):
1. Click on `Code` (It's green colour)
2. Click on `Download ZIP`
3. Save the file anywhere you want
4. Extract the ZIP folder
5. Create a .env file inside the extracted ZIP folder
6. In the .env file, type `download_path = PATH/TO/YOUR/DESIRED/LOCATION`

-----------------------------------------
# After all of prerequisites has been done:
1. Open Powershell
2. Type `cd PATH/TO/YOUR/EXTRACTED/ZIP`
3. Type `pip install -r requirements.txt`
4. Type `New-Item .env` (If you haven't done so already)

-----------------------------------------
## Finally, run main.py

# Creating a Batch File
## yt-dlp.bat
```
@py.exe "PATH/TO/main.py" %*
@pause
```
