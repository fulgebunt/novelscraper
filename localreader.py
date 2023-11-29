from flask import Flask, render_template, request, url_for, redirect
import json
import os
from main import download_more

from markupsafe import Markup

app = Flask(__name__)

# Assuming you have a list of JSON files in your 'static' directory
json_files = [f for f in os.listdir('static') if f.endswith('.json')]

@app.route("/")
def home():
    # Remove the .json extension from filenames
    display_files = [f[:-5] if f.endswith('.json') else f for f in json_files]
    return render_template('home.html', files=display_files)
@app.route("/download-chapters/<json_filename>/<int:current_chapter>")
def download_chapters(json_filename, current_chapter):
    download_more(json_filename)
    # Redirect to the current chapter of the novel
    return redirect(url_for('read', json_filename=json_filename, chapter_num=current_chapter))


@app.route("/read/<json_filename>")
@app.route("/read/<json_filename>/chapter/<int:chapter_num>")
def read(json_filename, chapter_num=1):
    # Construct file path and load JSON
    file_path = os.path.join('static', json_filename)
    if not os.path.exists(file_path):
        return "File not found.", 404
    with open(file_path, 'r') as file:
        chapters = json.load(file)

    # Get the chapter text
    chapter_key = f"Chapter {chapter_num}"
    chapter_text = chapters.get(chapter_key, "Chapter not found.")
    chapter_text = Markup(chapter_text.replace('\n', '<br>'))

    # Determine the availability of next and previous chapters
    next_chapter = chapter_num + 1 if f"Chapter {chapter_num + 1}" in chapters else None
    prev_chapter = chapter_num - 1 if chapter_num > 1 else None

    show_download_button = next_chapter is None  # True if there's no next chapter

    # Render the chapter text with navigation buttons
    return render_template('read.html', text=chapter_text, next_chapter=next_chapter, prev_chapter=prev_chapter, current_chapter=chapter_num, json_filename=json_filename, show_download_button=show_download_button)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9000)
