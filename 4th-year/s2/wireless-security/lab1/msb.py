def crc_msb_division(data_str, poly_str):
    # Padding data with the degree of the polynomial (4 zeros for x^4) 
    degree = len(poly_str) - 1
    padded_data = list(data_str + '0' * degree)
    poly = list(poly_str)
    
    print(f"--- Manual CRC Calculation (MSB First) ---")
    print(f"Generator Polynomial: {poly_str}")
    print(f"Initial Padded Data:  {''.join(padded_data)}\n")
    
    # Binary Division (Modulo-2 / XOR) [cite: 13]
    for i in range(len(data_str)):
        if padded_data[i] == '1':
            print(f"Step {i}: Found '1' at index {i}. XORing...")
            # Perform XOR against the generator
            for j in range(len(poly)):
                padded_data[i + j] = str(int(padded_data[i + j]) ^ int(poly[j]))
            print(f"   Result: {''.join(padded_data)}")
        else:
            print(f"Step {i}: Found '0' at index {i}. Skipping...")
            
    # The remainder is the ICV [cite: 13]
    remainder = ''.join(padded_data[-degree:])
    print(f"\nFinal ICV (Remainder): {remainder}")
    print(f"Plaintext + ICV to be encrypted: {data_str + remainder}")

# Input from your lab 
data = "10101010"
generator = "10011" # Corresponds to X^4 + X + 1

crc_msb_division(data, generator)