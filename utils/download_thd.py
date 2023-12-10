import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def download_image(url, save_path, max_retries=5, delay=5):
    for _ in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            if "429" in str(e):  # Retry on 429 errors
                print("Retrying after a delay...")
                time.sleep(delay)
                continue
            return False

def download_images(post_url, image_urls, save_folder):
    # Create a folder for each post
    post_id = post_url.split("/")[-1]
    post_folder = os.path.join(save_folder, post_id)
    os.makedirs(post_folder, exist_ok=True)

    # Download each image in the post
    for index, image_url in enumerate(image_urls, start=1):
        image_name = f"image_{index}.jpg"
        image_path = os.path.join(post_folder, image_name)
        download_image(image_url, image_path)

def download_with_delay(args):
    post_url, image_urls, save_folder, delay = args
    download_images(post_url, image_urls, save_folder)
    time.sleep(delay)  # Add delay between requests

if __name__ == "__main__":
    with open("extracted_hrefs.json", "r", encoding="utf-8") as json_file:
        extracted_hrefs = json.load(json_file)

    # Set the folder to save downloaded images
    save_folder = "../imgs"

    # Ensure the save folder exists
    os.makedirs(save_folder, exist_ok=True)

    # Set the delay between requests (in seconds)
    request_delay = 1

    # Set maximum retries and delay for 429 errors
    max_retries = 5
    retry_delay = 5

    # Prepare arguments for the download function
    download_args = [(post_url, image_urls, save_folder, request_delay) for post_url, image_urls in tqdm(extracted_hrefs.items(), desc="Preparing download")]

    # Download images with delay between requests and retries
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(download_with_delay, args) for args in download_args]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
            future.result()
