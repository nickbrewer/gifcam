from flask import Flask, render_template, request, redirect, Response
import os
import toml
import time
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
  return render_template('index.html')


@app.route('/gallery')
def gallery():
    # Get all files in the static/gifs/ directory
    all_files = os.listdir('static/gifs/')

    # Filter out only the .gif files
    all_image_names = [file for file in all_files if file.lower().endswith('.gif')]

    # Get the page query parameter from the request and convert it to an integer
    page = int(request.args.get('page', 1))

    # Calculate the start and end indices for the current page
    per_page = 5
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, len(all_image_names))

    # Get the subset of image names for the current page
    image_names = all_image_names[start_idx:end_idx]

    # Determine if there are more pages
    if end_idx < len(all_image_names):
        next_page = page + 1
    else:
        next_page = None

    # Determine if there is a previous page
    prev_page = page - 1 if page > 1 else None

    return render_template('gallery.html', image_names=image_names, prev_page=prev_page, next_page=next_page)


def load_config():
  with open('config.toml', 'r') as file:
    config = toml.load(file)
  return config

def save_config(config):
  with open('config.toml', 'w') as file:
    toml.dump(config, file)

@app.route('/config')
def config():
  config = load_config()
  return render_template('config.html', config=config)

@app.route('/update', methods=['POST'])
def update_config():
    config = load_config()
    for key, value in request.form.items():
        section, _, key = key.partition('-')  # Split the key into section and key
        if section in config and key in config[section]:
            # Convert the value to the appropriate type based on the existing config value type
            if isinstance(config[section][key], bool):
                config[section][key] = value.lower() == 'true'
            elif isinstance(config[section][key], int):
                config[section][key] = int(value)
            elif key == 'resolution':
                # Handle the resolution field as a tuple of integers
                try:
                    resolution_tuple = tuple(int(x.strip()) for x in value.strip('()').split(','))
                    if len(resolution_tuple) == 2:
                        config[section][key] = resolution_tuple
                except ValueError:
                    # Handle the case where the resolution field is not in the correct format
                    pass
            else:
                config[section][key] = value

    save_config(config)
    return redirect('/')

def generate_video():
    mp4_file_path = '/home/tom/gifcam/static/stream/preview_stream.mp4'

    # Open and read the MP4 file
    with open(mp4_file_path, 'rb') as video_file:
        # Read the entire MP4 file into memory
        video_data = video_file.read()

    # Yield the entire MP4 file as a single chunk
    yield video_data


@app.route('/preview')
def preview():
  return render_template('preview.html')

@app.route('/preview_video')
def preview_video():
    # Return the video file as a stream with MIME type 'video/h264'
    return Response(generate_video(), mimetype='video/mp4')
