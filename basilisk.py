
##___BASILISK___##

def basilisk(value):
    """ Basilisk is a rudementary 256 bit based hashing algorithim (modeled off of SHA 256). """
    
    binaryValue = binary(value)         #Converts input to binary
    paddedValue  = pad(binaryValue)     #Pads binary with 0's
    #print("Padded Binary Value:", paddedValue)                  

                                #Initial hash values (in hexadecimal)
                                #These values are derived from the first 32 bits of the fractional parts of the square roots of the 
    H = [                       #first 8 prime numbers.
        0x6a09e667,  #  H0   
        0xbb67ae85,  #  H1
        0x3c6ef372,  #  H2
        0xa54ff53a,  #  H3
        0x510e527f,  #  H4
        0x9b05688c,  #  H5
        0x1f83d9ab,  #  H6
        0x5be0cd19   #  H7
    ]

    K = [                       #Round constants: These constants are derived from the first 32 bits of the fractional parts of the 
                                #cube roots of the first 64 prime numbers.
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]


    for i in range(0,len(paddedValue),512):     #iterate through the padded value with 512 step (512 is the message block size)
        #print("Block", int(i/512))              #Print many 512 bit sized blocks there are

        block = paddedValue[i:i+512]            #Current 512-bit block of data
        W = binary_to_words(block)              #Convert block to 16   32-bit integers (words)
        #print(W)
        for t in range(16,64):
            #sigma functions are used in message expansion/scheduling to build W
            #Compute σ0 (sigma0) using right-rotates and shifts on W[t-15]
            s0 = rotr(W[t-15],7) ^ rotr(W[t-15], 18) ^ (W[t-15] >> 3)  #^ means XOR, >> means bitwise shift right. This loses bits and adds in 0s.

            #Compute σ1 (sigma1) using right-rotates and shifts on W[t-2]
            s1 = rotr(W[t-2], 17) ^ rotr(W[t-2], 19) ^ (W[t-2] >> 10)

             #Calculate W[t] based on earlier words and the two σ (sigma) values
            W.append((W[t-16] + s0 + W[t-7] + s1) & 0xFFFFFFFF)  # & 0xFFFFFFFF keeps it 32-bit
        
        #print("AFTER:", W)
        a, b, c, d, e, f, g, h = H  #Set the current hash state into working variables

        for t in range(64):  # 64 rounds total
            #SIGMA functions used here inside main loop on a and e variables for compression
            #Calculate upper-case Σ1 using bitwise right rotations of 'e'
            S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)

            #Choose bit: If e==1, use f, else use g (bitwise logic)
            ch = (e & f) ^ ((~e) & g) # & is bitwise AND,   ~ is bitwise NOT

            #Combine h, Σ1, choice, round constant, and message schedule word
            temp1 = (h + S1 + ch + K[t] + W[t]) & 0xFFFFFFFF  # Keep it 32 bits

            #Calculate upper-case Σ0 using bitwise right rotations of 'a'
            S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)

            #Majority function: majority of (a, b, c)
            maj = (a & b) ^ (a & c) ^ (b & c)

            #Calculate second temporary value
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h = g           #Each register shifts down
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF  #Update 'e' using temp1
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF  #New 'a' is total of temp1 and temp2

            H[0] = (H[0] + a) & 0xFFFFFFFF
            H[1] = (H[1] + b) & 0xFFFFFFFF
            H[2] = (H[2] + c) & 0xFFFFFFFF
            H[3] = (H[3] + d) & 0xFFFFFFFF
            H[4] = (H[4] + e) & 0xFFFFFFFF
            H[5] = (H[5] + f) & 0xFFFFFFFF
            H[6] = (H[6] + g) & 0xFFFFFFFF
            H[7] = (H[7] + h) & 0xFFFFFFFF

    digest = ''.join(f'{x:08x}' for x in H)  #Convert each 32-bit word into 8-character hex
    return "Hashed message: " + digest  #64 characters = 256 bits in hex


####   Helper functions:   ####

def binary(value):
    """ Convert input to binary """
    binaryValue = "".join(format(ord(char), "08b") for char in value)       
    return binaryValue

def pad(value):  
    """ Pads number with 0's """   

    if len(value) > 512:                                                    #If data is longer than 512 bits, and not divisible by 512 (or 8  if weird case), pad it
        while len(value) % 8 != 0:
            value += "0"
        while len(value) % 512 != 0:
            value += "0"

    if len(value) < 512:                                                    #If data is shorter than 512 bits, pad it
        for bit in range(0,(abs(512-len(value)))):
            value += "0"

    print(f"Length of value: {len(value)} bits")                            #Outputs the bits of the padded input
    return value

def split(value):
    chunkSize = int(len(value)/4)
    splitValues = []
    for i in range(4):
        start = (i*chunkSize)
        end = (start+chunkSize)
        splitValues.append(value[start:end])
    return splitValues

def rotr(x, n):                         
    """ ROTATES RIGHT a 32-bit word by n bits. The bits that fall off the right come back on the left. """

    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def binary_to_words(binary_str):        # "word" means a 32-bit chunk            
    """ Takes a binary string and splits it into 32-bit chunks, converts each to an integer. """

    return [int(binary_str[i:i+32], 2) for i in range(0, len(binary_str), 32)]




def main():
    userInput = str(input("Enter information to be hashed: "))
    print(basilisk(userInput))

if __name__ == "__main__":
    main()