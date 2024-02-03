import pandas as pd
import re
from pathlib import Path

# Define a function to parse the .dat file content and extract the required information
def parse_imgt_dat_file(file_path):
    # Define patterns to identify each section of the IMGT entry
    patterns = {
        'accession': re.compile(r'^AC\s+(.+);'),
        'v_gene_allele': re.compile(r'/allele="([^"]+)"'),
        'v_gene': re.compile(r'/gene="([^"]+)"'),
        'sequence': re.compile(r'^\s+([atgcATGC]+)\s+\d+$'),
        'translation': re.compile(r'/translation="([^"]+)"')
    }
    
    # Initialize variables to hold the data
    entries = []
    current_entry = {}
    
    # Read the file content
    with open(file_path, 'r') as file:
        for line in file:
            # Check for accession number
            if ac_match := patterns['accession'].search(line):
                current_entry['accession'] = ac_match.group(1)
            # Check for V-gene allele
            elif allele_match := patterns['v_gene_allele'].search(line):
                current_entry['v_gene_allele'] = allele_match.group(1)
            # Check for V-gene
            elif gene_match := patterns['v_gene'].search(line):
                current_entry['v_gene'] = gene_match.group(1)
            # Check for sequence data and concatenate it
            elif seq_match := patterns['sequence'].findall(line):
                current_entry['sequence'] = current_entry.get('sequence', '') + ''.join(seq_match)
            # Check for translation
            elif trans_match := patterns['translation'].search(line):
                current_entry['translation'] = trans_match.group(1).replace('\n', '').replace(' ', '')
            # Check for the end of an entry
            elif line.startswith('//'):
                # Add the current entry to the entries list
                entries.append(current_entry)
                # Reset the current entry
                current_entry = {}
    
    return entries

# Define the path to the .dat file (replace 'your_file_path.dat' with the actual file path)
# Since we don't have the actual .dat file, we'll just define a placeholder path
dat_file_path = '/path/to/your_file.dat'  # Placeholder path

# Parse the .dat file
imgt_data = parse_imgt_dat_file(dat_file_path)

# Convert the parsed data to a DataFrame
imgt_df = pd.DataFrame(imgt_data)

# Output the DataFrame to a CSV file
output_csv_path = '/mnt/data/imgt_data.csv'
imgt_df.to_csv(output_csv_path, index=False)

output_csv_path
