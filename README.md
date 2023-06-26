# Python-yt-dlp

`python-yt-dlp` is a wrapper for the [yt-dlp](https://github.com/yt-dlp/yt-dlp#readme) program that allows users to select their **resolution**, **fps**, and **video extension**. The program still runs via CLI but my intention is to run it via a Windows Batch File (`.bat`).

## Usage

1. Make sure Python is installed
2. Make sure 7zip is installed (used for installing step 3 -- recommended)
3. Make sure FFMPEG is installed
4. Download/Clone the repository
5. Create a `.env` file and store your `download_path`
6. Run `pip install -r requirements.txt`
7. Run `python main.py`

## Example of Batch File

``` bat
@py.exe "PATH/TO/main.py" %*
@pause
```
