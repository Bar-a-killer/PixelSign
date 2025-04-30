# PixelSign - Proof Inside your Pixel
# Copyright (c) 2024 江其恩
# Licensed under the MIT License
import hashlib
import cv2
import numpy as np
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import os
import argparse

def standardize_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    flat_img = img.flatten()
    flat_img = flat_img & np.uint8(254)  # 清空所有最低有效位
    img = flat_img.reshape(img.shape)
    return img

def generate_signature(image_path, private_key_path, stego_output_path):
    private_key = ECC.import_key(open(private_key_path).read())
    img = standardize_image(image_path)
    img_bytes = img.tobytes()
    hash_obj = SHA256.new(img_bytes)
    signer = DSS.new(private_key, 'fips-186-3')
    signature = signer.sign(hash_obj)
    flat_img = img.flatten()
    sig_bits = ''.join(format(byte, '08b') for byte in signature)
    if len(flat_img) < len(sig_bits):
        raise ValueError(f"圖片像素數量不足，至少需要 {len(sig_bits)} 個像素來藏簽章。")
        return 1
    for i, bit in enumerate(sig_bits):
        flat_img[i] = (flat_img[i] & np.uint8(254)) | int(bit)
    stego_img = flat_img.reshape(img.shape)
    cv2.imwrite(stego_output_path, cv2.cvtColor(stego_img, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sign and embed signature into image.')
    parser.add_argument('--image', required=True, help='Path to the original image')
    parser.add_argument('--key', required=True, help='Path to the private key PEM file')
    parser.add_argument('--output', required=True, help='Path to save the output stego image')
    args = parser.parse_args()

    generate_signature(args.image, args.key, args.output)
    print("簽章完成，已輸出帶簽章圖片。")

    #uv run .\signer.py --image images/original_image.png --key keys/private_key.pem --output images/stego_image.png