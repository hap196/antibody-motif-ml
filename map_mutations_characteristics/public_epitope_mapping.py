# This script finds all public epitopes and saves a spreadsheet of them

import csv

# Function to load patient data from CSV
def load_patient_counts_data(csv_path):
    """
    loads the patient data
    returns dict mapping of position of mutation to its count
    """
    pos_to_count = {}
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                pos = int(row['pos']) if row['pos'] else None
                counts = int(row['num_patients']) if row['num_patients'] else 0
            except ValueError:
                # Skip rows with invalid data
                continue
            
            pos_to_count[pos] = counts

    return pos_to_count

def find_public_epitopes(counts_data):
    """
    filter the counts. at least 30% of patients must have had that mutation
    return list of positions
    """
    total_num_patients = 232
    public_epitope_pos = []

    for pos, count in counts_data.items():
        if count/total_num_patients >= 0.2:
            public_epitope_pos.append(pos)

    return public_epitope_pos

# Function to load mutations data from CSV
def load_mutations_data(csv_path):
    pos_to_mutation = {}
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pos = int(row['i'])
            try:
                mutation = str(row['mutation'] if row['mutation'] else None)
                evescape_score = float(row['evescape']) if row['evescape'] else None
                counts = int(row['counts']) if row['counts'] else 0
                seen_date = row['first_seen'] if row['first_seen'] else None
            except ValueError:
                # Skip rows with invalid data
                continue
            mutation_data = {
                "mutation": mutation,
                "evescape_score": evescape_score,
                "counts": counts,
                "seen_date": seen_date
            }

            if pos not in pos_to_mutation:
                pos_to_mutation[pos] = [mutation_data]

            else:
                pos_to_mutation[pos].append(mutation_data)

    return pos_to_mutation

# Function to check for mutations
def map_mutation_to_evescape(public_epitopes, mutations_data):
    """
    given a list of positions of the public epitopes and a dictionary of dictionaries mapping position
    to mutation data, map the position of the epitope to the mutations data
    """
    epitope_pos_to_mutation = {}
    for pos in public_epitopes:
        if pos not in epitope_pos_to_mutation:
            epitope_pos_to_mutation[pos] = mutations_data[pos] if mutations_data[pos] is not None else None

        else:
            epitope_pos_to_mutation[pos] if mutations_data[pos] is not None else None

    return epitope_pos_to_mutation

# Function to save the found mutations to a CSV
def save_to_csv(found_mutations, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['position', 'evescape_score', 'counts', 'seen_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pos, data in found_mutations.items():
            print(pos)
            print(data)
            for i in range(len(data)):
                writer.writerow({'position': pos, 'evescape_score': data[i]['evescape_score'], 'counts': data[i]['counts'], 'seen_date': data[i]['seen_date']})

# Main function
def main():
    mutations_path = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 1\\spike_dist_one_scores_gisaid.csv"
    counts_path = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 2\\aaa_scanning_processed.csv"
    
    output_csv = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 2\\found_all_mutations.csv"  # Output CSV file path

    mutations_data = load_mutations_data(mutations_path)
    counts_data = load_patient_counts_data(counts_path)

    public_epitopes = find_public_epitopes(counts_data)
    # print(mutations_data)
    found_all_mutations = map_mutation_to_evescape(public_epitopes, mutations_data)
    #(found_mutations)
    #print(len(found_mutations))
    #print(len(sequence))
    print(found_all_mutations.items())
    save_to_csv(found_all_mutations, output_csv)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    main()
