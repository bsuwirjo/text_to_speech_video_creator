from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv
from os import listdir
from os.path import isfile, join
from moviepy.editor import *

class Video_Maker():
    def __init__(self, file_path):
        self.file_path = file_path
        self.name = file_path.split("/")[1]
        self.folder_path = '/'.join(file_path.split("/")[:2]) + '/'
        self.text = None
        self.chunk_length = 4000
        self.chunks = []

        # Load the .env file
        load_dotenv()

        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")

        # Ensure API key is available
        if not api_key:
            raise ValueError("API key not found. Please set OPENAI_API_KEY in the .env file.")

        # Initialize OpenAI client
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )

        self.client = OpenAI()
        self.read_file()
    
    # Function to get OpenAI response
    def convert_to_speech(self, file_name, text):
        speech_file_path = Path(__file__).parent / "stories" / self.name / file_name
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="ash",
            input=text,
        )
        response.stream_to_file(speech_file_path)
    
    def convert_all_to_speech(self):
        for i, text_chunk in enumerate(self.chunks):
            file_name = self.name + str(i) + ".mp3"
            caption_name = self.name + str(i) + ".srt"
            print("Converting chunk " + str(i) + " to " + file_name)
            self.convert_to_speech(file_name, text_chunk)
            print("Creating captions for, ", file_name)
            self.convert_speech_to_caption(self.folder_path + file_name, self.folder_path + caption_name)

    #Function to split text into 4000 character blocks
    def chunkstring(self):
        self.chunks = (self.text[0+i:self.chunk_length+i] for i in range(0, len(self.text), self.chunk_length))

    def read_file(self):
        with open(self.file_path, "r") as file:
            self.text = file.read().strip().replace("\n", "")
        
        #get optimal chunk length.
        while len(self.text) % self.chunk_length < 2000:
            self.chunk_length -= 100
        
        print("Using chunk length of ", self.chunk_length, ". Last chunk is ", len(self.text) % self.chunk_length)
    
    def convert_speech_to_caption(self, audio_file_path, caption_file_path):
        audio_file = open(audio_file_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="srt"
        )

        with open(caption_file_path, "a") as file:
            file.write(transcription)

    def combine_audio_video(self):
        background_clips = ["background_clips/" + f for f in listdir("background_clips") if isfile(join("background_clips", f))]
        print("Background Clips: ", background_clips)

        soundclips = [self.folder_path + f for f in listdir(self.folder_path) if isfile(join(self.folder_path, f)) and join(self.folder_path, f)[-4:] == ".mp3"]
        print("Sound Clips: ", soundclips)

        bclip_idx = 0

        for sclip in soundclips:
            name = sclip
            name = name[:-1] + '4'
            print("Creating " + name + " with " + sclip + " and " + background_clips[bclip_idx % len(background_clips)])

            videoclip = VideoFileClip(background_clips[bclip_idx % len(background_clips)])
            audioclip = AudioFileClip(sclip)

            videoclip.audio = audioclip.set_duration(videoclip.duration)
            videoclip = videoclip.loop(duration = audioclip.duration)
            videoclip.write_videofile(name)
            bclip_idx += 1