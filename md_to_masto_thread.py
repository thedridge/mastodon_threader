import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
from mastodon import Mastodon

# Initialize Mastodon
mastodon = Mastodon(
    access_token = 'your_api_token',
    api_base_url = 'https://your.instance.url'
)

def select_file():
    Tk().withdraw()
    filename = askopenfilename()
    return filename

def extract_posts_and_images(md_content):
    """
    Extract posts, local image paths, and alt text from markdown content.
    Returns a list of tuples where each tuple is (text, [(image_path, alt_text)]).
    """
    posts_with_images = []
    posts = md_content.split('\n\n')
    
    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    for post in posts:
        images = image_pattern.findall(post)
        # Filter out URLs, keeping only local file paths and capturing alt text
        local_images = [(img[1], img[0]) for img in images if not img[1].startswith('http')]
        # Remove image markdown from post text
        post_text = image_pattern.sub('', post).strip()
        posts_with_images.append((post_text, local_images))
    
    return posts_with_images

def upload_images(image_details):
    """
    Upload images with alt text and return their IDs for attaching to a post.
    image_details should be a list of tuples (image_path, alt_text).
    """
    media_ids = []
    for path, alt_text in image_details:
        try:
            media = mastodon.media_post(path, description=alt_text)
            media_ids.append(media['id'])
        except Exception as e:
            print(f"Failed to upload image {path}: {e}")
    return media_ids

def post_to_mastodon_with_images(posts_with_images):
    """
    Post messages and images to Mastodon with the first post public and the rest unlisted.
    """
    in_reply_to_id = None
    first_post = True
    for post_text, image_details in posts_with_images:
        media_ids = upload_images(image_details) if image_details else []
        visibility = 'public' if first_post else 'unlisted'
        try:
            response = mastodon.status_post(
                status=post_text,
                in_reply_to_id=in_reply_to_id,
                media_ids=media_ids,
                visibility=visibility  # First post public, rest unlisted
            )
            print(f"Posted: {post_text} with visibility {visibility}")
            in_reply_to_id = response['id']
            first_post = False  # Only the first post is public, subsequent posts are unlisted
        except Exception as e:
            print("An error occurred while posting:", e)

if __name__ == "__main__":
    md_file = select_file()
    if md_file:
        with open(md_file, 'r', encoding='utf-8') as file:
            md_content = file.read()
        posts_with_images = extract_posts_and_images(md_content)
        print("Posts to be sent:", posts_with_images)
        post_to_mastodon_with_images(posts_with_images)
