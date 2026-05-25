# List of alphabets used for shifting letters
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Keep program running until user decides to stop
text2 = False

while not text2:

    # Get encryption or decryption choice from user
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()

    # Get message and shift value
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    # Function to handle encoding and decoding
    def caesar(original_text, shift_amount, encode_or_decode):

        output_text = ""

        # Reverse shift for decoding
        if encode_or_decode == "decode":
            shift_amount *= -1

        # Process each letter in the message
        for letter in original_text:

            # Keep symbols, numbers, and spaces unchanged
            if letter not in alphabet:
                output_text += letter

            else:
                # Shift letter position
                shifted_position = alphabet.index(letter) + shift_amount
                shifted_position %= len(alphabet)

                # Add shifted letter to result
                output_text += alphabet[shifted_position]

        # Display final result
        print(f"Here is the {encode_or_decode}d result: {output_text}")

    # Call the Caesar cipher function
    caesar(original_text=text, shift_amount=shift, encode_or_decode=direction)

    # Ask user whether to continue or stop
    text1 = input("Type 'yes' to continue or 'no' to stop:\n").lower()

    if text1 == "no":
        text2 = True