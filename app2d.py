import random
from PIL import Image
import streamlit as st
import numpy as np
import time

def logistic_map(x, r):
    return r * x * (1 - x)

def generate_key(size):
    key = []
    for _ in range(size):
        key.append(random.random())
    return key

def encrypt_image(image, key, r):
    image_array = np.asarray(image)
    rows, cols, channels = image_array.shape

    encrypted_array = np.zeros_like(image_array, dtype=np.uint8)

    x = key[0]
    start_time = time.time()  # Start time measurement
    for i in range(rows):
        for j in range(cols):
            for k in range(channels):
                x = logistic_map(x, r)
                encrypted_array[i, j, k] = int((image_array[i, j, k] + 256 * x) % 256)
    end_time = time.time()  # End time measurement
    encryption_time = end_time - start_time

    encrypted_image = Image.fromarray(encrypted_array)
    return encrypted_image, key, encryption_time

def decrypt_image(encrypted_image, key, r):
    encrypted_array = np.asarray(encrypted_image)
    rows, cols, channels = encrypted_array.shape

    decrypted_array = np.zeros_like(encrypted_array, dtype=np.uint8)

    x = key[0]
    start_time = time.time()  # Start time measurement
    for i in range(rows):
        for j in range(cols):
            for k in range(channels):
                x = logistic_map(x, r)
                decrypted_array[i, j, k] = int((encrypted_array[i, j, k] - 256 * x) % 256)
    end_time = time.time()  # End time measurement
    decryption_time = end_time - start_time

    decrypted_image = Image.fromarray(decrypted_array)
    return decrypted_image, decryption_time

def main():
    st.title("Image Encryption and Decryption Using 2D Chaos Mapping")

    encryption_choice = st.selectbox("Choose an operation:", ["Encrypt", "Decrypt"])

    if encryption_choice == "Encrypt":
        st.subheader("Encryption")
        uploaded_image = st.file_uploader("Upload an image for encryption", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None:
            r = 3.9
            key_size = 1
            key = generate_key(key_size)
            st.write("Encryption Key:", key)
            encrypted_image, key_used, encryption_time = encrypt_image(Image.open(uploaded_image), key, r)
            st.image(encrypted_image, caption='Encrypted Image', use_column_width=True)
            encrypted_image_path = 'encrypted_image_2d.png'
            encrypted_image.save(encrypted_image_path)
            with open('key_2d.txt', 'w') as key_file:
                key_file.write(f'{key_used[0]}\n')
                key_file.write(f'{r}\n')
            st.write("Image encrypted successfully.")
            st.write(f"Encryption time: {encryption_time:.6f} seconds")
            st.write("Encryption key and parameter saved in key.txt.")
    elif encryption_choice == "Decrypt":
        st.subheader("Decryption")
        uploaded_encrypted_image = st.file_uploader("Upload the encrypted image", type=["jpg", "png", "jpeg"])
        uploaded_key_file = st.file_uploader("Upload the key file (key.txt)", type=["txt"])
        if uploaded_encrypted_image is not None and uploaded_key_file is not None:
            key = []
            lines = uploaded_key_file.readlines()
            key.append(float(lines[0].strip()))
            r = float(lines[1].strip())
            st.write("Decryption Key:", key)
            st.write("Logistic Map Parameter (r):", r)
            encrypted_image = Image.open(uploaded_encrypted_image)
            decrypted_image, decryption_time = decrypt_image(encrypted_image, key, r)
            st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)
            decrypted_image_path = 'decrypted_image_2d.png'
            decrypted_image.save(decrypted_image_path)
            st.write("Image decrypted successfully.")
            st.write(f"Decryption time: {decryption_time:.6f} seconds")

if __name__ == '__main__':
    main()
