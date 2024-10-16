# Read the file and remove trailing commas
with open('train_data.csv', 'r') as file:
    lines = file.readlines()

# Remove trailing commas and write back to the file
with open('train_data_cleaned.csv', 'w') as file:
    for line in lines:
        cleaned_line = line.rstrip(',\n') + '\n'  # Remove trailing comma and add newline
        file.write(cleaned_line)