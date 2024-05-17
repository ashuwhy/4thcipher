import string

main = string.ascii_lowercase

def generate_key(n, s):
    """
    Generates a numerical key matrix from a key string.
    """
    s = s.replace(" ", "").lower()
    key_matrix = ['' for _ in range(n)]
    i = 0
    j = 0
    for c in s:
        if c in main:
            key_matrix[i] += c
            j += 1
            if j > n - 1:
                i += 1
                j = 0

    print("The key matrix " + "(" + str(n) + 'x' + str(n) + ") is:")
    print(key_matrix)

    key_num_matrix = []
    for row in key_matrix:
        sub_array = []
        for j in range(n):
            sub_array.append(ord(row[j]) - ord('a'))
        key_num_matrix.append(sub_array)

    for row in key_num_matrix:
        print(row)
    return key_num_matrix


def message_matrix(s, n):
    """
    Converts a plaintext message into blocks of numerical values.
    """
    s = s.replace(" ", "").lower()
    final_matrix = []
    
    while len(s) % 4 != 0:
        s += 'a' 
    print("Converted plain_text for encryption: ", s)
    
    for k in range(len(s) // 4): 
        message_block = []
        for i in range(4):
            message_block.append(ord(s[i + (4 * k)]) - ord('a'))
        final_matrix.append(message_block)

    print("The blocks of plain text in numbers are:")
    for i in final_matrix:
        print(i)
    return final_matrix

def getCofactor(mat, temp, p, q, n):
    """
    Calculates the cofactor of an element in a matrix.
    """
    i = 0
    j = 0

    for row in range(n):
        for col in range(n):
            if row != p and col != q:
                temp[i][j] = mat[row][col]
                j += 1

                if j == n - 1:
                    j = 0
                    i += 1

def determinantOfMatrix(mat, n):
    """
    Calculates the determinant of a matrix.
    """
    D = 0
    if n == 1:
        return mat[0][0]

    temp = [[0 for x in range(n)] for y in range(n)]
    sign = 1

    for f in range(n):
        getCofactor(mat, temp, 0, f, n)
        D += (sign * mat[0][f] * determinantOfMatrix(temp, n - 1))
        sign = -sign
    return D

def isInvertible(mat, n):
    """
    Checks if a matrix is invertible.
    """
    return determinantOfMatrix(mat, n) != 0

def lilPreProcessing(block):
    """
    Applies pre-processing to a plaintext block.
    """
    sum_block = sum(block)
    avg = sum_block / 4
    block_adjustments = []
    
    for value in block:
        adjustment = value - avg
        block_adjustments.append(adjustment)
    
    return sum_block, block_adjustments

def create_blocks(message, block_size=4):
    """
    Creates blocks of ordinal values from a message.
    """
    message = message.lower().replace(" ", "")
    ord_values = [ord(char) - ord('a') for char in message]

    while len(ord_values) % block_size != 0:
        ord_values.append(0)

    blocks = [ord_values[i:i + block_size] for i in range(0, len(ord_values), block_size)]
    return blocks

def multiply_and_convert(key, message):
    """
    Performs matrix multiplication and modulo 26.
    """
    ciphertext = ""
    for i in range(len(message[0])):
        sum = 0
        for j in range(len(key)):
            sum += key[j][i] * message[0][j]
        ciphertext += chr((sum % 26) + 97) 
    return ciphertext

def lilPostProcessing(summed_values, adjustments):
    """
    Recovers the original plaintext blocks.
    """
    original_blocks = []

    for i, sum_block in enumerate(summed_values):
        avg = sum_block / 4
        block_adjustments = adjustments[i]
        original_block = [int(avg + adj) for adj in block_adjustments]
        original_blocks.append(original_block)
    
    return original_blocks

# --- Main Execution --- 
n = int(input("What will be the order of the square matrix: "))
s = input("Enter the key: ")
key = generate_key(n, s)

if isInvertible(key, len(key)):
    print("Yes, it is invertible and can be decrypted")
else:
    print("No, it is not invertible and cannot be decrypted")

plain_text = input("Enter the message: ")

# Pre-processing 
message_blocks = message_matrix(plain_text, n)
all_adjustments = [] 
ciphertext_sums = []
for block in message_blocks:
    sum_block, adjustments = lilPreProcessing(block)  
    all_adjustments.append(adjustments)
    ciphertext_sums.append(sum_block) 

# Hill Cipher Encryption 
final_message = multiply_and_convert(key, [ciphertext_sums])

print("Plain message: ", plain_text)
print("Final encrypted message: ", final_message)
print("Adjustments:", all_adjustments) 