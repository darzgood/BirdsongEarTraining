# Bird Song ID Track Generator

This project allows you to generate bird song recordings and their spoken names for a list of bird species.

It generates WAV audio files with each bird's song or call immediately followed by the bird's name.
I've found this is very useful for learning and memorizing bird songs as it reinforces correct ID's for birds immediately after hearing them.

Audio recordings are sourced from the Xeno-Canto library at <https://xeno-canto.org>.


## Instructions

1. Clone the repository:

   ```
   git clone https://github.com/your-username/bird-song-generator.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Prepare a text file with the list of bird species to retrieve audio for. Put each species' name on a separate line. For example:

   `Hardwood_Forest.txt`
   ```
   Black-Capped Chickadee
   Northern Cardinal
   Scarlet Tanager
   Tufted Titmouse
   White-breasted Nuthatch
   ```

4. Run the `habitat.py` Python script with the path to the text file as an argument:

   ```
   python habitat.py <path/to/bird_species.txt>
   ```

   Replace `<path/to/bird_species.txt>` with the actual path to your text file.

5. The script will retrieve the bird song recordings and generate spoken names for each bird species listed in the text file.

6. The generated audio files will be saved in a directory named the same as the text file. I.e `"Hardwood Forests/"`

7. You can now listen to the recordings and spoken names for each bird species.

Enjoy learning about the fascinating world of bird songs!
