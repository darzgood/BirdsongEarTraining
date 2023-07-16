import pickle
import random
import requests
import pyttsx3
from pydub import AudioSegment
import os
from gtts import gTTS

def get_TTS_engine():
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    # print (rate)                        #printing current voice rate
    engine.setProperty('rate', 125)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    # print (volume)                          #printing current volume level
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
	 #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

    return engine

def query_xeno_canto(species, query = "q:A len:5-60 type:song"):
    search_query = f"{species} {query}"
    search_url = f"https://www.xeno-canto.org/api/2/recordings?query={search_query}"
    response = requests.get(search_url)

    print(search_url)

    if response.status_code == 200:
        data = response.json()
        num_recordings = int(data.get('numRecordings', 0))

        if num_recordings > 0:
            return data['recordings']
        
    else:
        print(f"Internet Down or Link Invalid: {search_url}")

    return None

def search_song_urls(bird_species, samples = 1):
    """
    Species: str, single bird name, common or scientific
    samples: int, number of urls to return

    Returns: song_urls, songnames
     List: URls of files to download
     List: Common name associated with each url
    """

    song_urls = []
    song_names = []

    for species in bird_species:
        
        recordings = query_xeno_canto(species)
        if(recordings == None):
            ### Try reducing constraints if first query is empty
            recordings = query_xeno_canto(species, query = "q:A len:1-90")
        
        if recordings:
            chosen_recordings = random.choices(recordings, k = samples)
            for recording in chosen_recordings:
                song_urls.append(recording['file'])
                song_names.append(recording['en'])
        
        else:
            print(f"Audio recordings retrieval failed: {species}" )
            
    return song_urls, song_names

def generate_audio_file(engine, phrase, output_file):
    #engine = pyttsx3.init()
    engine.save_to_file(phrase, output_file)
    engine.runAndWait()

def generate_audio_file_gtts(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

def concatenate_audio_files(song_file, pronunciation_file, output_file):
    song = AudioSegment.from_file(song_file)
    pronunciation = AudioSegment.from_file(pronunciation_file)

    combined = song + pronunciation
    combined.export(output_file, format='wav')

def save_bird_song(name, url, subdirectory, engine):
    spoken_name = f"{name.replace(' ', '_')}_name.wav"
    song_output = f"{name.replace(' ', '_')}_song.wav"

    # Generate name audio locally
    generate_audio_file(engine, name, spoken_name)
    # OR use google's TTS
    # generate_audio_file_gtts(name, spoken_name)

    # Download a song
    response = requests.get(url)
    with open(song_output, 'wb') as f:
        f.write(response.content)

    # Combine the two!
    combined_output = os.path.join(subdirectory, f"{name.replace(' ', '_')}.wav")
    concatenate_audio_files(song_output, spoken_name, combined_output)

    # Delete the leftover audio clips
    os.remove(spoken_name)
    os.remove(song_output)

def generate_bird_songs(bird_names, habitat="Default", season="all", samples=1):
    """
    Creates an audio file for a list of bird with
     1. A sample of their song from Xeno-Canto 
     2. The species name appended to the end for easy playback.

    Args:
        bird_names (list): A list of the birds to be added.
        habitat (str): The subfolder name to add the birds to! (default: "Default").
        season (str): What time of year to target. Options: "all", "spring", "fall", "winter", "summer" (default: "all").
        samples (int): How many recordings for each species (default: 1).

    Returns:
        None

    TODO:
        - Implement season filtering logic.
        - Retrieve multiple recordings for each species.
    """

    # song_urls = get_bird_song_urls(bird_names)

    song_urls, song_names = search_song_urls(bird_names, samples)
    engine = get_TTS_engine()

    # Create a subdirectory for the combined output files
    subdirectory = habitat
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    # Combine each song and name and save it!
    for name, url in zip(song_names, song_urls):
        if url:
            save_bird_song(name, url, subdirectory, engine)
            print(f"Combined audio generated for '{name}'")
        else:
            print(f"No song URL found for '{name}'")

    engine.stop()


### Example
# bird_species = ["Chipping Sparrow", "Pine Warbler", "Acadian Flycatcher", "Worm-eating Warbler"]
# generate_bird_songs(bird_species)