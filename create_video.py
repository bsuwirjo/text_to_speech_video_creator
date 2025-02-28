import sys
from video_maker import Video_Maker

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid number of arguments, usage: create_video.py foldername, title, text")
        exit()

    file_path = sys.argv[1]


    video_maker = Video_Maker(file_path)

    if video_maker.chunkstring() == 0:
        print("Error importing and chunking text")
        exit()

    if video_maker.convert_all_to_speech() == 0:
        print("Error converting text to speech")
        exit()

    if video_maker.combine_audio_video() == 0:
        print("Error combining video and audio")
        exit()
    
    print("Videos successfully created, they can be found here: " + file_path + " ending with .mp4.")