import requests
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    with open("../jsons/post_urls.json", "r", encoding="utf-8") as json_file:
        post_urls = json.load(json_file)

    with open("extracted_hrefs.txt", "w", encoding="utf-8") as href_file:
        for post_url in post_urls:
            post_response = requests.get(post_url)
            soup = BeautifulSoup(post_response.content, "html.parser")

            # 查找所有类似<a>标签的内容，且class="fileThumb"
            file_thumb_links = soup.find_all("a", class_="fileThumb")

            for link in file_thumb_links:
                # 提取链接的href属性并写入文件
                file_url = link.get("href")
                href_file.write(file_url + "\n")

                print(f"Extracted: {file_url}")

    print("Extraction completed. Check extracted_hrefs.txt for the links.")
