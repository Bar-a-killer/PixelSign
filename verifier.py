# PixelSign - Proof Inside your Pixel
# Copyright (c) 2024 江其恩
# Licensed under the MIT License
import hashlib
import cv2
import numpy as np
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import argparse

def standardize_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    flat_img = img.flatten()
    flat_img = flat_img & np.uint8(254)  # clear the lowest bit
    img = flat_img.reshape(img.shape)
    return img

def extract_signature(img_path, signature_length):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    flat_img = img.flatten()
    extracted_bits = [str(flat_img[i] & 1) for i in range(signature_length * 8)]
    extracted_bytes = bytes(int(''.join(extracted_bits[i:i+8]), 2) for i in range(0, len(extracted_bits), 8))
    return extracted_bytes

def verify_signature(stego_image_path, public_key_path, signature_length):
    public_key = ECC.import_key(open(public_key_path).read())
    extracted_signature = extract_signature(stego_image_path, signature_length)
    img = standardize_image(stego_image_path)
    img_bytes = img.tobytes()
    hash_obj = SHA256.new(img_bytes)
    verifier = DSS.new(public_key, 'fips-186-3')
    try:
        verifier.verify(hash_obj, extracted_signature)
        print("驗證成功：圖片已經認證")
    except ValueError:
        print("驗證失敗：圖片未被驗證或被竄改")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify the signature embedded in an image.')
    parser.add_argument('--image', required=True, help='Path to the stego image')
    parser.add_argument('--key', required=True, help='Path to the public key PEM file')
    args = parser.parse_args()
    signature_length = 64 #should be change if we use other sign tec in the future
    
    verify_signature(args.image, args.key, signature_length)

#uv run verifier.py --image images/stego_image.png --key keys/testcode_public_key.pem
