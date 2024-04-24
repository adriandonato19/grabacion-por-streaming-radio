import requests
import time
import datetime
import os
import json

def load_urls_from_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

def download_audio(url, folder_path):
    while True:
        start_time = time.time()  # Start time for each download attempt
        current_time = datetime.datetime.now()
        subfolder_path = os.path.join(folder_path, current_time.strftime('%Y'), current_time.strftime('%m'), current_time.strftime('%d'))
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(subfolder_path, f"{current_time.strftime('%Y%m%d_%H%M%S')}.wav")
        with open(file_path, 'wb') as file:
            response = requests.get(url, stream=True)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                elapsed_time = time.time() - start_time
                if elapsed_time > 1200:  # Check if 20 minutes (1200 seconds) have passed
                    remaining_time = 1200 - elapsed_time
                    if remaining_time > 0:
                        time.sleep(remaining_time)  # Wait for the remaining time of the 20-minute block
                    break

def main():
    urls = load_urls_from_json("emisoras.json")

    for radio_name, url in urls.items():
        folder_path = os.path.join(os.getcwd(), radio_name.replace(" ", "_"))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        download_audio(url, folder_path)
        print(f"Downloaded audio from {radio_name}")

if __name__ == "__main__":
    main()
