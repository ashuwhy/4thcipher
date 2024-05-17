import string
import numpy as np

main = string.ascii_lowercase

def generate_key(n, s):
    s = s.replace(" ", "")
    s = s.lower()

    key_matrix = ['' for i in range(n)]
    i = 0
    j = 0
    for c in s:
        if c in main:
            key_matrix[i] += c
            j += 1
            if(j > n - 1):
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
    plain_text = plain_text.replace(" ", "").lower()
    padding_length = 4 - (len(plain_text) % 4)
    if padding_length != 4:
        plain_text += 'a' * padding_length
    print("Padded plaintext: ", plain_text)
    
    groups = [plain_text[i:i+4] for i in range(0, len(plain_text), 4)]
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
    return sums, RNKs, plain_text

def hill_cipher_encrypt(key_matrix, sums):
    sums_vector = np.array(sums).reshape(-1, len(key_matrix))
    key_matrix = np.array(key_matrix)
    cipher_vector = np.dot(sums_vector, key_matrix) % 26
    cipher_text = ''.join([chr(int(num) + ord('a')) for num in cipher_vector.flatten()])
    return cipher_text

def hill_cipher_decrypt(key_matrix, cipher_text):
    cipher_vector = np.array([ord(c) - ord('a') for c in cipher_text]).reshape(-1, len(key_matrix))
    key_matrix = np.array(key_matrix)
    det = int(round(np.linalg.det(key_matrix))) % 26
    det_inv = pow(det, -1, 26)
    adjugate_matrix = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    inv_key_matrix = (det_inv * adjugate_matrix) % 26
    decrypted_vector = np.dot(cipher_vector, inv_key_matrix) % 26
    sums = decrypted_vector.flatten().astype(int).tolist()
    return sums

def reconstruct_plaintext(sums, RNKs):
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
    sums, RNKs, padded_text = pre_process(plain_text)
    cipher_text = hill_cipher_encrypt(key_matrix, sums)
    return cipher_text, RNKs

def decrypt_4th_cipher(cipher_text, key_matrix, RNKs):
    sums = hill_cipher_decrypt(key_matrix, cipher_text)
    decrypted_text = reconstruct_plaintext(sums, RNKs)
    return decrypted_text

# Input and function calls
n = int(input("What will be the order of the square matrix: "))
s = input("Enter the key: ")
key = generate_key(n, s)

plain_text = input("Enter the message: ")
cipher_text, RNKs = encrypt_4th_cipher(plain_text, key)
print("Encrypted message: ", cipher_text)

decrypted_text = decrypt_4th_cipher(cipher_text, key, RNKs)
print("Decrypted message: ", decrypted_text)
