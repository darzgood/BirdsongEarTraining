import sys
import os

from generate_audio_files import generate_bird_songs

def extract_bird_names(habitat_filename):
    bird_names = []
    with open(habitat_filename, 'r') as file:
        for line in file:
            bird_names.extend(line.strip().split(','))

    return bird_names

def get_words_from_filename(filename):
    file_name, _ = os.path.splitext(filename)
    words = file_name.split('_')  # Assuming words are separated by underscores
    return words

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a habitat filename as an argument.")
        sys.exit(1)

    habitat_filename = sys.argv[1]
    bird_names = extract_bird_names(habitat_filename)

    habitat = " ".join(get_words_from_filename(habitat_filename)).title()

    generate_bird_songs(bird_names, habitat)
