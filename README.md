## The 4thCipher: A Hill Cipher Enhancement

**Abstract:**  The 4thCipher, developed by [ashuwhy](https://github.com/ashuwhy/), introduces a novel pre-processing technique to enhance the security and efficiency of the Hill cipher. This method utilizes a unique encoding scheme that embeds crucial decryption information within the plaintext itself, eliminating the need for separate key transmission while preserving the integrity of the original Hill cipher algorithm.  The cipher leverages matrix operations to encrypt multiple blocks of encoded plaintext simultaneously, increasing efficiency.

**1. Introduction:**

The Hill cipher, a classic symmetric encryption algorithm, utilizes matrix multiplication for encryption. While inherently secure, its vulnerability to known-plaintext attacks and the need for secure key exchange remain challenges. The 4thCipher addresses these concerns by introducing a pre-processing layer that obfuscates the plaintext before Hill cipher application, thereby enhancing its resilience against cryptanalysis.

**2. The Algorithm:**

**2.1 Pre-processing (Encoding):**

1. **Padding:** If the plaintext length is not a multiple of four, append 'a' characters to achieve the desired length.
2. **Grouping:** Divide the padded plaintext into groups of four letters.
3. **Summation:** For each group, calculate the sum of the ordinal values (A=0, B=1, …, Z=25) of the constituent letters.
4. **Real Number Key (RNK) Generation:**
   - Compute the average of the sum for each group (sum/4).
   - For each letter in the group, subtract the average from the letter's ordinal value. These differences constitute the RNK for the respective group. 

**2.2 Hill Cipher Application:**

1. **Key Matrix:** Define a square key matrix (e.g., 2x2, 3x3) and ensure it is invertible for decryption.
2. **Sum Padding:**  Pad the list of sums with zeros until the length of the list is a multiple of the number of columns in the key matrix. 
3. **Matrix Reshaping:** Arrange the padded sums list into a matrix where the number of columns matches the number of columns in the key matrix. The number of rows will be automatically determined. 
4. **Matrix Multiplication:**  Multiply the reshaped sums matrix by the key matrix.
5. **Modulo 26:** Apply the modulo 26 operation to each element of the resulting matrix.
6. **Ciphertext Generation:** Convert the numerical values in the resulting matrix back into letters to form the ciphertext. 

**2.3 Decryption:**

1. **Inverse Key Matrix:** Compute the inverse of the key matrix.
2. **Ciphertext Decryption:** Convert the ciphertext back into numerical values and arrange them into a matrix matching the dimensions of the ciphertext matrix from encryption. Multiply this ciphertext matrix by the inverse key matrix. Apply modulo 26 to the result to recover the original padded sums matrix.
3. **RNK Retrieval:** The receiver is provided with the corresponding RNK values.
4. **Ordinal Value Reconstruction:** For each group:
   - Extract the sum for the group from the decrypted sums matrix.
   - Calculate the average of the sum.
   - Add the respective RNK values to the average to recover the original ordinal values of each letter. 
5. **Plaintext Formation:** Convert the recovered ordinal values back into letters to reconstruct the original plaintext.

**3. Examples:**

**3.1 Example 1 (2x2 Key Matrix):**

* Plaintext: `gptivo`
* Key Matrix: 
  ```
  [3, 5]
  [2, 7]
  ```
1. **Pre-processing:**
   - Padded plaintext: `gptivoaa`
   - Group 1: (g, p, t, i) → (6, 15, 19, 8) → Sum = 48, Average = 12, RNK = [-6, 3, 7, -4]
   - Group 2: (v, o, a, a) → (21, 14, 0, 0) → Sum = 35, Average = 8.75, RNK = [12.25, 5.25, -8.75, -8.75]
2. **Hill Cipher Application:**
   - Sums: [48, 35] 
   - Reshaped Sums Matrix: [[48, 35]]
   - Ciphertext vector = [[48, 35]] * [[3, 5], [2, 7]] = [[214, 485]]  (mod 26) = [[6, 17]] = `gr` 
3. **Decryption:**
   - Receiver obtains ciphertext: `gr` and RNK: [[-6, 3, 7, -4], [12.25, 5.25, -8.75, -8.75]] 
   - Decrypt `gr` to [[214, 485]] using the inverse key matrix.
   - Reconstruct original ordinal values using the averages (12, 8.75) and the RNK.
   - Recover plaintext: `gptivo`.

**3.2 Example 2 (2x2 Key Matrix):**

* Plaintext: `hill`
* Key Matrix:
  ```
  [3, 5]
  [2, 7]
  ```
1. **Pre-processing:**
   - Padded plaintext: `hillaaa`
   - Group 1: (h, i, l, l) → (7, 8, 11, 11) → Sum = 37, Average = 9.25, RNK = [-2.25, -1.25, 1.75, 1.75]
   - Group 2: (a, a, a, a) → (0, 0, 0, 0) → Sum = 0, Average = 0, RNK = [0, 0, 0, 0]
2. **Hill Cipher Application:**
   - Sums: [37, 0]
   - Reshaped Sums Matrix: [[37, 0]] 
   - Ciphertext vector = [[37, 0]] * [[3, 5], [2, 7]] = [[111, 185]]  (mod 26) = [[7, 3]] = `hd` 
3. **Decryption:**
   - Receiver obtains ciphertext: `hd` and RNK: [[-2.25, -1.25, 1.75, 1.75], [0, 0, 0, 0]]
   - Decrypt `hd` to [[111, 185]] using the inverse key matrix.
   - Reconstruct original ordinal values using the averages (9.25, 0) and the RNK.
   - Recover plaintext: `hill`.

**3.3 Example 3 (3x3 Key Matrix):**

* Plaintext: `code`
* Key Matrix:
  ```
  [17, 17, 5] 
  [21, 18, 21]
  [ 2,  2, 19]
  ```
1. **Pre-processing:**
   - Padded plaintext: `codeaaaa`
   - Group 1: (c, o, d, e) → (2, 14, 3, 4) → Sum = 23, Average = 5.75, RNK = [-3.75, 8.25, -2.75, -1.75]
   - Group 2: (a, a, a, a) → (0, 0, 0, 0) → Sum = 0, Average = 0, RNK = [0, 0, 0, 0]
2. **Hill Cipher Application:**
   - Sums: [23, 0]
   - Padded Sums: [23, 0, 0]
   - Reshaped Sums Matrix: [[23, 0, 0]]
   - Ciphertext vector = [[23, 0, 0]] * [[17, 17, 5], [21, 18, 21], [2, 2, 19]] = [[391, 391, 115]] (mod 26) = [[19, 19, 11]] = `ttl`
3. **Decryption:**
   - Receiver obtains ciphertext: `ttl` and RNK: [[-3.75, 8.25, -2.75, -1.75], [0, 0, 0, 0]]
   - Decrypt `ttl` to [[391, 391, 115]] using the inverse key matrix.
   - Reconstruct original ordinal values using the averages (5.75, 0) and the RNK.
   - Recover plaintext: `code`.

**3.4 Example 4 (3x3 Key Matrix):**

* Plaintext: `helloworld`
* Key Matrix:
  ```
  [ 2,  4, 12] 
  [ 9, 13,  6]
  [ 7,  0, 14]
  ```
1. **Pre-processing:**
   - Padded plaintext: `helloworldaaaa`
   - Group 1: (h, e, l, l) → (7, 4, 11, 11) → Sum = 33, Average = 8.25, RNK = [-1.25, -4.25, 2.75, 2.75]
   - Group 2: (o, w, o, r) → (14, 22, 14, 17) → Sum = 67, Average = 16.75, RNK = [-2.75, 5.25, -2.75, 0.25]
   - Group 3: (l, d, a, a) → (11, 3, 0, 0) → Sum = 14, Average = 3.5, RNK = [7.5, -0.5, -3.5, -3.5]
   - Group 4: (a, a, a, a) → (0, 0, 0, 0) → Sum = 0, Average = 0, RNK = [0, 0, 0, 0]
2. **Hill Cipher Application:**
   - Sums: [33, 67, 14, 0]
   - Reshaped Sums Matrix: 
     ```
     [[33, 67, 14]
      [ 0,  0,  0]] 
     ```
   - Ciphertext matrix =  [[33, 67, 14], [0, 0, 0]] * [[ 2,  4, 12], [ 9, 13,  6], [ 7,  0, 14]] = [[759, 1005, 582], [0, 0, 0]]  (mod 26) = [[1, 25, 14] [0, 0, 0]] = `bzoaaa` 
3. **Decryption:**
   - Receiver obtains ciphertext: `bzoaaa` and RNKs.
   - Decrypt `bzoaaa` to [[759, 1005, 582], [0, 0, 0]] using the inverse key matrix. 
   - Reconstruct original ordinal values using group averages and RNKs.
   - Recover plaintext: `helloworld`.

**4. Security Analysis:**

The 4thCipher's strength lies in its ability to:

* **Obscure Plaintext:** The RNK encoding effectively masks the original plaintext, making performing frequency analysis or other known-plaintext attacks challenging.
* **Implicit Key Exchange:** By embedding the RNK within the plaintext modification, the 4thCipher eliminates the need for separate secure key exchange for these values.
* **Efficiency of Matrix Operations:** By applying the Hill cipher to the entire encoded message simultaneously, the cipher leverages the efficiency of matrix multiplication.

However, vulnerabilities remain:

* **Key Matrix Security:** The Hill cipher key matrix remains a critical element and must be kept secret.
* **RNK Pattern Analysis:** If an attacker intercepts multiple ciphertexts encrypted with the same key, they may be able to identify patterns in the RNK and exploit them for decryption.

**5. Conclusion:**

The 4thCipher presents a promising refinement to the Hill cipher, enhancing its security and efficiency through a clever pre-processing method and matrix operations. While vulnerabilities persist, the embedded RNK approach significantly strengthens the algorithm's resistance to known plaintext attacks and simplifies key management. I encourage further research and analysis to explore the 4thCipher's full potential and address the remaining security concerns. 
