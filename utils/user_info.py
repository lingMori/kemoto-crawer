import requests
from bs4 import BeautifulSoup
import json

def generate_post_urls(user_id, start_page, end_page, page_form):
    base_url = f"https://kemono.su/fanbox/user/{user_id}"

    # Initialize an empty list to store complete post URLs
    post_urls = []

    for page_index in range(start_page, end_page + 1):
        src_url_pages = f"{base_url}?o={page_index * page_form}"
        src_response = requests.get(src_url_pages)
        soup = BeautifulSoup(src_response.content, 'html.parser')

        # Find all links with the specified pattern
        post_links = [a['href'] for a in soup.find_all('a', href=lambda href: href and f'/fanbox/user/{user_id}/post/' in href)]

        # Combine base URL with each post link and add to the list
        post_urls.extend([f"https://kemono.su{post_link}" for post_link in post_links])

    return post_urls, post_links

def save_urls_to_json(data, file_name):
    # Save the data to a JSON file
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    user_id = "6641844"
    start_page = 1
    end_page = 5
    page_form = 50

    post_urls, post_links = generate_post_urls(user_id, start_page, end_page, page_form)
    
    # Save post URLs to JSON
    save_urls_to_json(post_urls, "../jsons/post_urls.json")
    print("Post URLs saved to post_urls.json")

    # Save post links to JSON
    save_urls_to_json(post_links, "../jsons/post_links.json")
    print("Post links saved to post_links.json")
