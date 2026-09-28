# Image Encryption and Decryption using Chaos Mapping

A Python project that scrambles an image into unreadable noise and then restores it exactly, using a secret key. It includes two interactive **Streamlit** web apps and a simple command-line version.

| Script | Interface | Technique |
|--------|-----------|-----------|
| `app2d.py` | Streamlit web app | Chaos-based encryption using the **logistic map** |
| `app.py` | Streamlit web app | XOR stream cipher with a random 1024-byte key |
| `imageenc.py` | Command line | XOR stream cipher with a random 1024-byte key and a password-protected key file |

`flower.png` is a sample image you can use for testing.

---

## How it works

### 1. Chaos mapping with the logistic map (`app2d.py`)

The logistic map is a simple equation that behaves chaotically:

```
x(n+1) = r · x(n) · (1 − x(n))
```

With `r = 3.9`, the sequence of `x` values looks random, but it is fully determined by the starting value `x0`. A tiny change to `x0` produces a completely different sequence, which is what makes it useful as a key.

**Encryption**
1. A random seed `x0` in (0, 1) is generated. This is the secret key.
2. The image is loaded as a NumPy array of shape `(rows, cols, channels)`.
3. For every pixel channel, the map is iterated once to get the next `x`, and the value is shifted:
   `encrypted = (pixel + 256·x) mod 256`
4. The encrypted image is saved as `encrypted_image_2d.png`, and `x0` and `r` are saved to `key_2d.txt`.

**Decryption**
1. You upload the encrypted image and `key_2d.txt`.
2. The same chaotic sequence is regenerated from `x0` and `r`.
3. Each value is shifted back: `pixel = (encrypted − 256·x) mod 256`.
4. The original image is restored and saved as `decrypted_image_2d.png`.

### 2. XOR stream cipher (`app.py` and `imageenc.py`)

1. A key of 1024 random bytes (0–255) is generated.
2. The raw image bytes are XOR-ed with the key, which repeats cyclically: `enc[i] = img[i] ^ key[i % 1024]`.
3. Because XOR undoes itself, running the same operation with the same key restores the original image.
4. The key is saved to `key.txt`, one number per line. In `imageenc.py`, the first line of the file is a password that must be entered correctly before decryption.

Both apps display the encryption and decryption time so the methods can be compared.

---

## Getting started

### Requirements
- Python 3.8+
- `streamlit`, `pillow`, `numpy`

```bash
pip install streamlit pillow numpy
```

### Run the web apps

```bash
streamlit run app2d.py   # logistic-map chaos encryption
streamlit run app.py     # XOR encryption
```

Then open the URL Streamlit prints (usually http://localhost:8501):
1. Choose **Encrypt** and upload an image. The encrypted image appears, and the key file is written to the project folder.
2. Choose **Decrypt**, then upload the encrypted PNG and its key file to get the original back.

### Run the CLI version

```bash
python imageenc.py
```

Enter the image path, then use the menu: `1` encrypts (and asks you to set a password), `2` decrypts (and asks for the password), `3` exits.

---

## Notes and limitations

- **Always save encrypted images as PNG.** JPEG compression is lossy and would corrupt the encrypted pixels, so decryption would fail.
- `app2d.py` expects colour images with a channel dimension (RGB or RGBA). Grayscale images need converting first.
- The logistic-map version loops over every pixel in pure Python, so large images can take a while.
- This is an educational project demonstrating chaos-based cryptography. It is not intended for securing sensitive data.

## Tech stack
Python · Streamlit · Pillow (PIL) · NumPy
