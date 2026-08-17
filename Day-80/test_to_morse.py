from morse_data import morse_code

text = input("Enter Your word: ").upper()

morse = []
for char in text:
    if char.isalpha():
        morse.append(morse_code[char])
    else:
        morse.append(char)

morse_text = " ".join(morse)
print(morse_text)