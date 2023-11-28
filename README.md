# Image Auto-Converter to WebP

## Description

This project is a Python script that automatically converts images in a specified folder to the WebP format. It watches a folder (e.g., the Downloads folder) and converts any new images to WebP, potentially reducing file size while maintaining or improving image quality.

## Features

- Automatic conversion of images to WebP format.
- System tray integration for easy control.
- Options to pause/resume conversion and delete original files.
- Logging of conversion processes and memory usage.

## Setup and Installation

To set up this project, follow these steps:

1. Clone the repository:

`git clone https://github.com/andrewnx/autowebp`

2. Navigate to the project directory:

`cd [project directory]`

3. Install the required dependencies:

`pip install -r requirements.txt`

4. To run the script, use the following command:

`python autowebp.py`

## How It Works

The script uses the Watchdog library to monitor a specified directory for new image files. When a new image is detected, it's automatically converted to the WebP format. The Pystray library is used for system tray integration, allowing the user to pause/resume the conversion process and toggle the deletion of original files.
