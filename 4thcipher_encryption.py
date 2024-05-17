import string
import numpy as np

main = string.ascii_lowercase

def generate_key(n, s):
    """Generates a numerical key matrix from a key string."""
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
    for i in key_matrix:
        sub_array = []
        for j in range(n):
            sub_array.append(ord(i[j]) - ord('a'))
        key_num_matrix.append(sub_array)

    for i in key_num_matrix:
        print(i)
    return key_num_matrix

def pre_process(plain_text):
    """Pads plaintext and calculates sums and RNKs."""
    plain_text = plain_text.replace(" ", "").lower()
    padding_length = 4 - (len(plain_text) % 4)
    if padding_length != 4:
        plain_text += 'a' * padding_length
    print("Padded plaintext: ", plain_text)

    groups = [plain_text[i:i+4] for i in range(0, len(plain_text), 4)]
    if len(groups) % 2 != 0:
        groups.append('aaaa')
    print("Groups: ", groups)

    sums = []
    RNKs = []
    for group in groups:
        ord_values = [ord(c) - ord('a') for c in group]
        group_sum = sum(ord_values)
        group_avg = group_sum / 4
        RNK = [ord_value - group_avg for ord_value in ord_values]
        sums.append(group_sum)
        RNKs.append(RNK)

    print("Sums: ", sums)
    print("RNKs: ", RNKs)
    return sums, RNKs

def hill_cipher_encrypt(key_matrix, sums):
    """Encrypts the sums using the Hill cipher."""
    # Pad sums to match key matrix columns
    while len(sums) % len(key_matrix[0]) != 0:
        sums.append(0)
    
    # Reshape sums into a matrix 
    sums_vector = np.array(sums).reshape(-1, len(key_matrix[0])) 
    print("Modified sums_vector:\n", sums_vector)  # Show the modified sums_vector

    key_matrix = np.array(key_matrix)
    cipher_vector = np.dot(sums_vector, key_matrix) % 26
    cipher_text = ''.join([chr(int(num) + ord('a')) for num in cipher_vector.flatten()])
    return cipher_text

def reconstruct_plaintext(sums, RNKs):
    """Reconstructs the plaintext from sums and RNKs."""
    reconstructed_text = ""
    for i in range(len(sums)):
        group_sum = sums[i]
        RNK = RNKs[i]
        group_avg = group_sum / 4
        ord_values = [round(group_avg + rnk) for rnk in RNK]
        reconstructed_group = ''.join([chr((ord_value % 26) + ord('a')) for ord_value in ord_values])
        reconstructed_text += reconstructed_group
    return reconstructed_text

def encrypt_4th_cipher(plain_text, key_matrix):
    """Encrypts plaintext using the 4th cipher method."""
    sums, RNKs = pre_process(plain_text)
    cipher_text = hill_cipher_encrypt(key_matrix, sums)
    return cipher_text, RNKs

def getCofactor(mat, temp, p, q, n):
    """Calculates the cofactor of an element in a matrix."""
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
    """Calculates the determinant of a matrix."""
    D = 0
    if n == 1:
        return mat[0][0]

    temp = [[0 for x in range(n)] for y in range(n)]
    sign = 1

    for f in range(n):
        getCofactor(mat, temp, 0, f, n)
        D += sign * mat[0][f] * determinantOfMatrix(temp, n - 1)
        sign = -sign
    return D

def isInvertible(mat, n):
    """Checks if a matrix is invertible."""
    return determinantOfMatrix(mat, n) != 0

# Input and function calls
n = int(input("What will be the order of the square matrix: "))
s = input("Enter the key: ")
key = generate_key(n, s)

if isInvertible(key, n):
    print("Yes, the key matrix is invertible and can be used for encryption.")
else:
    print("No, the key matrix is not invertible. Please choose another key.")

plain_text = input("Enter the message: ")
cipher_text, RNKs = encrypt_4th_cipher(plain_text, key)
print("Encrypted message: ", cipher_text)