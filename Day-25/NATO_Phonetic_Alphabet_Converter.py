import pandas as pd

# Read NATO phonetic alphabet CSV file
reading_csv = pd.read_csv("nato_phonetic_alphabet.csv")

# Create dictionary in the format:
# {"A": "Alfa", "B": "Bravo", ...}
csv_dict = {
    key.letter: key.code
    for (index, key) in reading_csv.iterrows()
}

# Get user input and convert it to uppercase
user_input = input("Enter a string: ").upper()

# Convert each letter into its NATO code word
output_list = [
    csv_dict[alpha]
    for alpha in user_input
]

# Display the final NATO code list
print(output_list)