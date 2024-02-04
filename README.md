# Markdown to Mastodon Thread Poster

This Python script allows users to post content from a markdown file to Mastodon, including images with alt text, and set the visibility of posts directly through the markdown file's front matter. 
### Disclaimer:
The script was written using a process that relied heavily on GPT-4 to generate the code. It has been tested a few times on a small instance and it works, but feel free to improve it as you see fit. 

## Features

- **Markdown Parsing:** Converts markdown content into Mastodon posts.
- **Image Uploads:** Includes local images in posts with specified alt text.
- **Visibility Control:** Sets post visibility (`public`, `unlisted`, `private`, `direct`) via markdown front matter.

## Prerequisites

Ensure you have Python 3.x installed on your system. This script requires the following Python packages:

- `PyYAML` for YAML front matter parsing.
- `Mastodon.py` for interacting with the Mastodon API.
- `tkinter` for file selection dialogs.

*Note: You may want to create a virtual environment before installing PyYAML and Mastodon.py. I had to run it in a virtual environment.*

Once your venv is created and activated, install the required packages using pip:

```bash
pip install PyYAML Mastodon.py
```

## Setup

1. **Mastodon API Access Token and Instance URL:** Obtain an access token from your Mastodon instance and replace `your_api_token` and `https://your.instance.url` in the script with your actual token and Mastodon instance URL.

2. **Markdown File Format:** Your markdown file should start with YAML front matter for setting post visibility, enclosed in `---`. Example:

```markdown
---
visibility: unlisted
---
This is post number 1. When you add two consecutive line breaks it will create the next toot in the thread.

This is the beginning of the second toot in the thread. You can add an image using the standard markdown image embed format. The caption will be added as alt text. ![Image Alt Text](path/to/image.jpg)

This will be the third toot in the thread. End of Thread!
```

## Usage

1. Run the script:

```bash
python3 md_to_masto_thread.py
```

2. Select the markdown file you wish to post when prompted.


## Security

Do not commit your Mastodon API token or instance URL to GitHub. Always replace these with placeholders when sharing your script.
