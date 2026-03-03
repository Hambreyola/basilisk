# Basilisk

Basilisk is a rudementary 256 bit based hashing algorithim (modeled off of SHA 256) written in python. 
<br>
<br>
<br>
### CORE PROCESS:
1. Take input, convert to binary and pad it
2. Set up 8   32-bit registers as constants (H) and 64 32-bit word constants (K)
3. For each 256 bit block, create the first 16x 32 bit words (W[0]-W[15]) using bitwise math
4. Expand to 64 words (W[16]-W[63]) using the σ₀/σ₁ (small sigma) functions and earlier W values.
5. Over 64 rounds, the state is updated with lots of bitwise math
6. Output digest as hex

<br>
<br>

### POTENTIAL FUTURE IMPROVEMENTS:
+ Some algorithims out there (Bcrypt) have a work factor which greatly improves the security of hashed data
+ Salt and/or Pepper 
+ SHA-256, the algorithim I modeled this off, of appends the length of the value to be padded at the end of the binary padded value.
+ I did minimal avalanche testing, more avalanche testing should be conducted to spot possible issues

<br>
<br>

### FLOWCHART:
Input  →  Binary  →  Padding  →  512-bit blocks

↓↓↓

Each 512-bit block:

 ├─> 16x 32-bit words (W[0]-W[15])

 ├─> Expand to 64 words (W[16]-W[63]) using σ₀, σ₁

 ├─> Iterate 64 rounds with Σ₀, Σ₁, Ch, Maj, K[t]

 └─> Update hash values (H0-H7)

↓↓↓

Final Digest (64 hex chars / 256 bits)
<br>
<br>
<br>


### DEFINITIONS :
Word	        
A 32-bit unsigned (no + or - sign) integer

Rotate (rotr)    
Rotates bits to the right, preserving all bits

W[0..63]	    
64 words per block, built from input and mixed with bitwise operations

a..h	    
Working registers used during hashing

Ch, Maj	        
Bitwise choice and majority functions used to add complexity/scramble data

S0, S1	        
Uppercase sigmas: derived from rotates to mix bits

Temp1/2	        
Temporary values that determine how the state changes

H[0..7]	        
Final hash values built up by modifying initial constants

Rotations and XORs reduce avalanche effect and create bit diffusion (every bit of the message affects every bit of the final hash.)

<br>
<br>

### FORMULAS

S1  = Σ₁(e)
ch  = (e AND f) XOR ((NOT e) AND g)
temp1 = h + S1 + ch + K[t] + W[t]

S0  = Σ₀(a)
maj = (a AND b) XOR (a AND c) XOR (b AND c)
temp2 = S0 + maj

h = g

g = f

f = e

e = (d + temp1) mod 2³²

d = c

c = b

b = a

a = (temp1 + temp2) mod 2³²

What each part does:

Σ₀, Σ₁	                                    
Uppercase sigmas	   
Rotate/bit-mix the working variables

Ch (choice)	(e & f) ^ (~e & g)        
Selects bits from f or g depending on e

Maj (majority)	(a & b) ^ (a & c) ^ (b & c)	       
Outputs the majority bit among a,b,c

K[t]	   
Round constant	    
Provides fixed, non-repeating bias per round

W[t]    
Message word	  
Brings in message-dependent entropy


\+	                                        
32-bit modular addition	[makes it wrap-around arithmetic (with the mod 2³²)]

After processing all 64 rounds:

H[0] = (H[0] + a) mod 2³²

H[1] = (H[1] + b) mod 2³²

. . .

H[7] = (H[7] + h) mod 2³²

Last, concatenate the 8 × 32-bit words to produce the final 256-bit digest:

digest = H[0] ‖ H[1] ‖ H[2] ‖ H[3] ‖ H[4] ‖ H[5] ‖ H[6] ‖ H[7]

In hexadecimal form, this yields 64 hex characters
(since each hex digit = 4 bits -> 64 × 4 = 256 bits).

<br>
<br>



### BITWISE MATH       
ROTRⁿ(x)	                        
((x >> n)	(x << (32 - n))) & 0xFFFFFFFF

SHRⁿ(x)	x >> n	                   
 Logical right shift (fills with zeros)

XOR	a ^ b	                       
 Combine differing bits (bitwise mix)

AND	a & b	                       
 Bitwise filtering

NOT	~a	         
                   Bitwise inversion

σ₀, σ₁	      
        (See above)	Expand message schedule

Σ₀, Σ₁	          
      (See above)	Mix working variables each round

Ch	(e & f) ^ (~e & g)	    
        Bit-wise conditional select

Maj	(a & b) ^ (a & c) ^ (b & c)	    
Majority function

\+ (mod 2³²)	                    
    Modular addition - Prevents overflow beyond 32 bits
<br>
<br>

### PURPOSE OF BITWISE MATH
+ Rotations + shifts = bit shuffling
+ XORs = combine patterns, erase linearity
+ AND/NOT = conditional branching of bits
+ Adds mod 2³² = maintain randomness while staying 32-bit
+ Repeated 64 rounds = diffusion of input bits
+ Final H values = the 256-bit digest
