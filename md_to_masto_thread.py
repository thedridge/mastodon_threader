import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
import yaml  # Ensure PyYAML is installed
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

def read_md_front_matter(file_path):
    """
    Reads the YAML front matter from the markdown file to extract metadata.
    If no front matter is present, returns None for metadata and the full content.
    
    Parameters:
        file_path (str): Path to the markdown file.
    
    Returns:
        tuple: A tuple containing metadata (as a dict or None if no front matter is present)
               and the markdown content (str).
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        if content.startswith("---"):
            # Attempt to split the content into front matter and markdown content
            parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) > 2:
                front_matter, md_content = parts[1], parts[2]
                try:
                    metadata = yaml.safe_load(front_matter)
                except yaml.YAMLError as e:
                    print("Error parsing YAML front matter:", e)
                    metadata = None
                md_content = md_content.strip()  # Ensure we remove leading/trailing whitespace
            else:
                # No valid front matter found, treat the entire content as markdown
                metadata = None
                md_content = content
        else:
            # No front matter delimiter found, treat the entire content as markdown
            metadata = None
            md_content = content
    
    return metadata, md_content



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

def post_to_mastodon_with_images(posts_with_images, visibility='public'):
    """
    Post messages and images to Mastodon with specified visibility.
    """
    in_reply_to_id = None
    for post_text, image_details in posts_with_images:
        media_ids = upload_images(image_details) if image_details else []
        try:
            response = mastodon.status_post(
                status=post_text,
                in_reply_to_id=in_reply_to_id,
                media_ids=media_ids,
                visibility=visibility  # Set the visibility of the post
            )
            print(f"Posted: {post_text} with visibility {visibility}")
            in_reply_to_id = response['id']
        except Exception as e:
            print("An error occurred while posting:", e)



if __name__ == "__main__":
    md_file = select_file()
    if md_file:
        metadata, md_content = read_md_front_matter(md_file)
        visibility = metadata.get('visibility', 'public')  # Default to 'public' if not specified
        posts_with_images = extract_posts_and_images(md_content)
        print("Posts to be sent:", posts_with_images)
        post_to_mastodon_with_images(posts_with_images, visibility)

