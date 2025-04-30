# PixelSign - Proof Inside your Pixel
# Copyright (c) 2024 江其恩
# Licensed under the MIT License
from Crypto.PublicKey import ECC
import os
import argparse

def generate_keys(name, private_dir='keys', public_dir='keys'):
    os.makedirs(private_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)
    key = ECC.generate(curve='P-256')
    private_key_path = os.path.join(private_dir, f'{name}_private_key.pem')
    public_key_path = os.path.join(public_dir, f'{name}_public_key.pem')
    with open(private_key_path, 'wt') as f:
        f.write(key.export_key(format='PEM'))
    with open(public_key_path, 'wt') as f:
        f.write(key.public_key().export_key(format='PEM'))
    print(f"私鑰已儲存至: {private_key_path}")
    print(f"公鑰已儲存至: {public_key_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate private and public keys.')
    parser.add_argument('--name', required=True, help='Name identifier for the key files')
    args = parser.parse_args()

    generate_keys(args.name)
    print("金鑰生成完成。")