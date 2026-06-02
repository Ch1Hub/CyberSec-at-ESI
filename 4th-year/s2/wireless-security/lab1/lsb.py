def crc_teacher_lsb(data_str, poly_str):
    # 1. Adding the 4 zeros to the data normally
    degree = len(poly_str) - 1
    padded_normal = data_str + ('0' * degree)
    
    # 2. Reflect the data (including the padded zeros)
    reflected_input = padded_normal[::-1]
    
    print(f"--- Teacher's LSB Approach ---")
    print(f"Normal Padded:    {padded_normal}")
    print(f"Reflected Input:  {reflected_input}")
    print(f"Generator (MSB):  {poly_str}\n")
    
    # 3. Apply normal MSB division on the reflected data
    working_bits = list(reflected_input)
    poly = list(poly_str)
    
    # Division loop
    for i in range(len(working_bits) - degree):
        if working_bits[i] == '1':
            print(f"Step {i}: XORing at position {i}")
            for j in range(len(poly)):
                working_bits[i + j] = str(int(working_bits[i + j]) ^ int(poly[j]))
            print(f"   State: {''.join(working_bits)}")
        else:
            # In your teacher's example 000001010101, 
            # the first 5 steps will be 'skipping'
            print(f"Step {i}: Bit is 0, skipping...")
            
    remainder = ''.join(working_bits[-degree:])
    print(f"\nFinal ICV (LSB Remainder): {remainder}")
    return remainder

# Inputs
data = "10101010"
generator = "10011"

crc_teacher_lsb(data, generator)