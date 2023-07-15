import pickle
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


# Get Scientific names
pkl_file = 'species_mapping.pkl'
def load_species_mapping(pkl_file):
    with open(pkl_file, 'rb') as f:
        species_mapping = pickle.load(f)
    return species_mapping





def get_bird_song_urls(bird_species):
    ###
    # This function is still very much a work in progress 
    # Ideally it would find the best available audio recording
    # Of the right species!!! (Check scientific name and subspecies, etc)
    # Quality: A
    # Length: 10-15 seconds in length
    # Song type: Song (rather than call or drum or other)
    # 
    # The order that these criterion can be relaxed needs to be more thought out
    # 
    # Additionally, it would be great to return a list of possible urls, and then a separate function can randomly sample a few.

    ###

    song_urls = []
    background_sp = []

    print("Downloading Songs: ...", end ="")

    # english_to_scientific = load_species_mapping(pkl_file)

    for species in bird_species:
        ### Initially tried to convert to scientific to be more precise, but with taxonomic name changes, etc, this was a bust.
        # try:
        #     search_query = f"{english_to_scientific[species]} q:A len:5-60 type:song"
        # except KeyError:
        #     search_query = f"{species} q:A len:5-60 type:song"

        search_query = f"{species} q:A len:5-60 type:song"

        search_url = f"https://www.xeno-canto.org/api/2/recordings?query={search_query}"
        response = requests.get(search_url)

        if response.status_code == 200:
            data = response.json()

            if int(data['numRecordings']) > 0:
                if data['recordings'][0]['en'] != species:
                    print("Oops! The song of a {} was almost downloaded instead of {}. You may have to download this audio manually!".format(data['recordings'][0]['en'], species))
                    song_urls.append(None)
                else:
                    song_url = data['recordings'][0]['url']
                    song_urls.append("https:{}".format(song_url))
            else:
                song_urls.append(None)

                ### Should actually retry with less stringent query
        else:
            song_urls.append(None)
        
        print(".", end ="")

    print(" ")

    return song_urls

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
    response = requests.get(url+"/download")
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

    song_urls = get_bird_song_urls(bird_names)
    engine = get_TTS_engine()

    # Create a subdirectory for the combined output files
    subdirectory = habitat
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    # Combine each song and name and save it!
    for name, url in zip(bird_names, song_urls):
        if url:
            save_bird_song(name, url, subdirectory, engine)
            print(f"Combined audio generated for '{name}'")
        else:
            print(f"No song URL found for '{name}'")

    engine.stop()


### Example
# bird_species = ["Chipping Sparrow", "Pine Warbler", "Dark-eyed Junco", "Alder Flycatcher", "American Goldfinch", "American Robin",
#                 "Brown Creeper", "Black-and-white Warbler", "Cedar Waxwing", "Eastern Bluebird", "Red-winged Blackbird", "Willow Flycatcher"]
# generate_bird_songs(bird_species)