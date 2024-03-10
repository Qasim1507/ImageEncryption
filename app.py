import random
from PIL import Image
import streamlit as st

def generate_key(size):
    key = []
    for _ in range(size):
        key.append(random.randint(0, 255))
    return key

def encrypt_image(image, key):
    image_data = image.tobytes()
    
    encrypted_data = bytearray()
    for i in range(len(image_data)):
        encrypted_data.append(image_data[i] ^ key[i % len(key)])
    
    encrypted_image = Image.frombytes(image.mode, image.size, bytes(encrypted_data))
    
    return encrypted_image, key

def decrypt_image(encrypted_image, key):
    encrypted_data = encrypted_image.tobytes()
    
    decrypted_data = bytearray()
    for i in range(len(encrypted_data)):
        decrypted_data.append(encrypted_data[i] ^ key[i % len(key)])
    
    decrypted_image = Image.frombytes(encrypted_image.mode, encrypted_image.size, bytes(decrypted_data))
    
    return decrypted_image

def main():
    st.title("Image Encryption and Decryption Using Chaos Mapping")
    
    encryption_choice = st.selectbox("Choose an operation:", ["Encrypt", "Decrypt"])
    
    if encryption_choice == "Encrypt":
        st.subheader("Encryption")
        uploaded_image = st.file_uploader("Upload an image for encryption", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None:
            key_size = 1024
            key = generate_key(key_size)
            st.write("Encryption Key:", key)
            encrypted_image, key_used = encrypt_image(Image.open(uploaded_image), key)
            st.image(encrypted_image, caption='Encrypted Image', use_column_width=True)
            encrypted_image_path = 'encrypted_image.png'
            encrypted_image.save(encrypted_image_path)
            with open('key.txt', 'w') as key_file:
                for k in key_used:
                    key_file.write(f'{k}\n')
            st.write("Image encrypted successfully.")
            st.write("Encryption key saved in key.txt.")
            st.download_button(label="Download Encrypted Image", data=open(encrypted_image_path, 'rb').read(), file_name='encrypted_image.png', mime='image/png')
            st.download_button(label="Download Encryption Key", data=open('key.txt', 'rb').read(), file_name='key.txt', mime='text/plain')
    elif encryption_choice == "Decrypt":
        st.subheader("Decryption")
        uploaded_encrypted_image = st.file_uploader("Upload the encrypted image", type=["jpg", "png", "jpeg"])
        uploaded_key_file = st.file_uploader("Upload the key file (key.txt)", type=["txt"])
        if uploaded_encrypted_image is not None and uploaded_key_file is not None:
            key = []
            for line in uploaded_key_file:
                try:
                    key.append(int(line.strip()))
                except ValueError:
                    # Skip non-integer lines
                    pass
            st.write("Decryption Key:", key)
            encrypted_image = Image.open(uploaded_encrypted_image)
            decrypted_image = decrypt_image(encrypted_image, key)
            st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)
            decrypted_image_path = 'decrypted_image.png'
            decrypted_image.save(decrypted_image_path)
            st.write("Image decrypted successfully.")
            st.download_button(label="Download Decrypted Image", data=open(decrypted_image_path, 'rb').read(), file_name='decrypted_image.png', mime='image/png')

if __name__ == '__main__':
    main()
