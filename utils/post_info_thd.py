import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def extract_hrefs(post_url):
    try:
        post_response = requests.get(post_url)
        soup = BeautifulSoup(post_response.content, "html.parser")
        file_thumb_links = soup.find_all("a", class_="fileThumb")
        extracted_hrefs = [link.get("href") for link in file_thumb_links]
        return post_url, extracted_hrefs
    except Exception as e:
        print(f"Error processing {post_url}: {e}")
        return post_url, []

if __name__ == "__main__":
    with open("../jsons/post_urls.json", "r", encoding="utf-8") as json_file:
        post_urls = json.load(json_file)

    # 使用多线程提取数据
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for result in tqdm(executor.map(extract_hrefs, post_urls), total=len(post_urls), desc="Extracting"):
            results.append(result)

    # 构建结果字典
    result_dict = {url: hrefs for url, hrefs in results}

    # 写入JSON文件
    with open("extracted_hrefs.json", "w", encoding="utf-8") as json_file:
        json.dump(result_dict, json_file, ensure_ascii=False, indent=2)

    print("Extraction completed. Check extracted_hrefs.json for the links.")
