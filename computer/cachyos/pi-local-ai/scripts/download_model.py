#!/usr/bin/env python3
"""Download GGUF models from Hugging Face."""

import argparse
import os
from huggingface_hub import HfApi, hf_hub_download, login, whoami

def main():
    parser = argparse.ArgumentParser(description='Download GGUF models from Hugging Face')
    parser.add_argument('repo_id', help='Repository ID (e.g., unsloth/Phi-3.5-mini-instruct-4k-GGUF)')
    parser.add_argument('filename', help='Filename to download (e.g., phi-3.5-mini-instruct-4k-Q4_K.gguf)')
    parser.add_argument('--local-dir', default='./models', help='Local directory to save file')
    parser.add_argument('--token', help='Hugging Face token (optional, will prompt if needed)')
    args = parser.parse_args()

    # Create local directory
    os.makedirs(args.local_dir, exist_ok=True)

    # Check if already logged in
    try:
        user = whoami()
        print(f"Logged in as: {user['name']}")
    except:
        # Try to login
        if args.token:
            login(token=args.token)
        else:
            print("Not logged in. Run 'huggingface-cli login' or provide --token")
            login()

    # Download file
    print(f"Downloading {args.filename} from {args.repo_id}...")
    local_path = hf_hub_download(
        repo_id=args.repo_id,
        filename=args.filename,
        local_dir=args.local_dir,
        local_dir_use_symlinks=False
    )
    print(f"Downloaded to: {local_path}")
    print(f"File size: {os.path.getsize(local_path) / (1024**3):.2f} GB")

if __name__ == '__main__':
    main()
