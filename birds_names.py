import pandas as pd
import pickle

def create_species_mapping(excel_file, output_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Create a dictionary to store the species mapping
    species_mapping = {}

    # Iterate over the rows of the DataFrame
    for _, row in df.iterrows():
        common_name = row['English name']
        scientific_name = row['scientific name']

        # Skip rows with missing common or scientific names
        if pd.isnull(common_name) or pd.isnull(scientific_name):
            continue

        # Add the mapping to the dictionary
        species_mapping[common_name] = scientific_name

    # Save the dictionary as a pickled file
    with open(output_file, 'wb') as f:
        pickle.dump(species_mapping, f)

    print(f"Species mapping created and saved to '{output_file}'.")

# Example usage
excel_file = 'Clements-v2022-October-2022.xlsx'
output_file = 'species_mapping.pkl'
create_species_mapping(excel_file, output_file)


def load_species_mapping(pkl_file):
    with open(pkl_file, 'rb') as f:
        species_mapping = pickle.load(f)
    return species_mapping
