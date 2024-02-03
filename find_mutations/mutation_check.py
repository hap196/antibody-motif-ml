import csv

# Sample sequence extracted from the image
# 766 - 835
sequence = "ALTGIAVEQKQNTVEQFAVQKJYKTPPIKDFGGFNFSQILPDPKSRSFIEDLLFNKVTLADGFIK"

# Function to load mutations data from CSV
def load_mutations_data(csv_path):
    mutations_data = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mutation = row['mutation']
            try:
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
            mutations_data.append(mutation_data)
    return mutations_data

# Function to check for mutations
def check_for_mutations(sequence, mutations_data, start_pos, end_pos):
    results = {}
    for data in mutations_data:
        mutation = data['mutation']
        original_amino_acid = mutation[0]
        try:
            position = int(mutation[1:-1])
        except ValueError:
            print(f"Invalid mutation format: {mutation}")
            continue
        mutated_amino_acid = mutation[-1]
        if (start_pos <= position <= end_pos) and (position - start_pos < len(sequence)):
            if sequence[position - start_pos] == mutated_amino_acid:
                results[mutation] = {'original_aa': original_amino_acid, 'position': position, 'mutated_aa': mutated_amino_acid, 'evescape_score': data['evescape_score'], 'counts': data['counts'], 'seen_date': data['seen_date']}
    return results

# Function to save the found mutations to a CSV
def save_to_csv(found_mutations, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['mutation', 'evescape_score', 'counts', 'seen_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for mutation, data in found_mutations.items():
            writer.writerow({'mutation': mutation, 'evescape_score': data['evescape_score'], 'counts': data['counts'], 'seen_date': data['seen_date']})

# Main function
def main():
    csv_path = "C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 1\\spike_dist_one_scores_gisaid.csv"
    output_csv = "found_mutations.csv"  # Output CSV file path
    start_pos = 766
    end_pos = 835
    mutations_data = load_mutations_data(csv_path)
    # print(mutations_data)
    found_mutations = check_for_mutations(sequence, mutations_data, start_pos, end_pos)
    #(found_mutations)
    #print(len(found_mutations))
    #print(len(sequence))
    print(found_mutations.items())
    save_to_csv(found_mutations, output_csv)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    main()
