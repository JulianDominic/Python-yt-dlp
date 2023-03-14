from yt_dlp import YoutubeDL

def get_info(URL:str):
    """This function extracts the video's information regarding its (i) resolution, (ii) video extension, (iii) audio extension, and (iv) fps. We return a 'video_set' which is a tuple that contains the different resolution, video extension, and fps combinations available for download. We drop certain video extensions such as 3gp. This function also assumes that we are only inputting 1 video rather than a playlist."""
    with YoutubeDL() as ydl:
        info = ydl.extract_info(URL, download=False)
        # ydl.list_formats(info)
        format_info = info['formats']

        main_sets = {
                    "vext": {"mp4", "mov", "webm", "flv", "mkv"},
                    "aext": {"m4a", "aac", "mp3", "ogg", "opus", "webm"},
                    }

        res_set = set()
        vext_set = set()
        aext_set = set()

        video_set = set()

        for information in format_info:
            aext = information["audio_ext"]
            aext_set.add(aext)
            try:
                res = information["format"]
                res = clean_res(res)
                if not(res):
                    continue
            except KeyError:
                continue
            vext = information["video_ext"]
            if vext not in main_sets["vext"]:
                continue
            
            fps = information["fps"]
            video_info = (res, vext, fps)

            res_set.add(res)
            vext_set.add(vext)

            video_set.add(video_info)
            
        res_set = sorted(res_set)
        vext_set = sorted(main_sets["vext"].intersection(vext_set))
        aext_set = sorted(main_sets["aext"].intersection(aext_set))
        video_set = sorted(video_set)

        return res_set, vext_set, aext_set, video_set


def get_options(res_set:list, vext_set:list, video_set:list) -> dict:
    """This function takes in the resolutions, video extensions, and the different combinations available from get_info in order to package them nicely into different dictionaries where the main key is the resolution whose values are video extensions that contain the different fps values."""
    res_options = {}
    for resolution in res_set:
        vext_options = {}
        for vext in vext_set:
            vext_options[vext] = []
            for item in video_set:
                if item[0] == resolution and item[1] == vext:
                    vext_options[vext].append(item[2])
        res_options[resolution] = vext_options
        
    return res_options
    

def clean_res(res: str):
    """This function cleans up the output we get from 'format_info' in get_info. A typical output would look something like '22 - 960x720 (720p)' which we will turn into '720'."""
    start, end, cout = 0, 0, 0
    for char in res:
        if char == "(":
            start = cout + 1
        elif char == ")":
            end = cout
        cout += 1

    res = res[start:end]
    res = res.replace("HDR", "")
    res = res.replace("p60", "")
    res = res.replace("p", "")
    
    try:
        res = int(res)
        return res
    except ValueError:
        return False