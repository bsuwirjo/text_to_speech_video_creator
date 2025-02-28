from pytubefix import YouTube
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid number of arguments, usage: video_downloader.py folder, url")
        exit()

    folder = sys.argv[1]
    url = sys.argv[2]
    

    yt = YouTube(url)
    yt_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    #yt_video = yt.streams.filter(only_video=True, mime_type="video/mp4").order_by('resolution').desc().first().download(filename="video.mp4")
    yt_video.download(folder)
    print("Successfully downloaded video.")