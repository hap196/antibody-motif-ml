import csv
import re

# Increase the maximum field size limit
csv.field_size_limit(2**31 - 1)

# Compile regex patterns once
patterns = {
    'AC': re.compile(r'^AC\s+(.+?);'),
    'FT_allele': re.compile(r'/allele="(.+?)"'),
    'FT_gene': re.compile(r'/gene="(.+?)"'),
    'FT_translation': re.compile(r'/translation="(.+?)"')
}

# Function to parse the .dat file
def parse_dat_file(dat_file_path):
    dat_info = {}
    with open(dat_file_path, 'r') as file:
        for line in file:
            if line.startswith('AC'):
                ac_match = patterns['AC'].search(line)
                if ac_match:
                    current_ac = ac_match.group(1).strip()
                    dat_info[current_ac] = {'v_gene_allele': '', 'v_gene': '', 'translation': ''}
            elif 'FT' in line:
                if '/allele=' in line:
                    allele_match = patterns['FT_allele'].search(line)
                    if allele_match:
                        dat_info[current_ac]['v_gene_allele'] = allele_match.group(1).strip()
                elif '/gene=' in line:
                    gene_match = patterns['FT_gene'].search(line)
                    if gene_match:
                        dat_info[current_ac]['v_gene'] = gene_match.group(1).strip()
                elif '/translation=' in line:
                    translation_match = patterns['FT_translation'].search(line)
                    if translation_match:
                        dat_info[current_ac]['translation'] = translation_match.group(1).strip().replace(' ', '')
    return dat_info

# Define the path to your files
csv_file_path = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 4\\v_gene_sequences_heavy_chain.csv"
dat_file_path = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 4\\imgt.dat"  # Replace this with the path to 
output_file_path = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 4\\v_gene_information.csv"

# Parse the .dat file once and store the information
dat_info = parse_dat_file(dat_file_path)

# Read the CSV file and write to the new CSV file
with open(csv_file_path, mode='r') as csvfile, open(output_file_path, mode='w', newline='') as outfile:
    csv_reader = csv.reader(csvfile)
    csv_writer = csv.writer(outfile)
    next(csv_reader, None)  # skip the headers
    csv_writer.writerow(['accession_id', 'v_gene_name', 'v_gene_allele', 'sequence', 'translation'])
    
    for row in csv_reader:
        accession_id = row[0].split('|')[0].strip()
        sequence = row[1].strip()
        entry = dat_info.get(accession_id, {})
        csv_writer.writerow([accession_id, entry.get('v_gene'), entry.get('v_gene_allele'), sequence, entry.get('translation')])