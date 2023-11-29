from flask import Flask, render_template
from markupsafe import Markup
import json

app = Flask(__name__)

# Load the chapters from JSON file
with open('libraryofheaven.json', 'r') as file:
    chapters = json.load(file)

def add_html_line_breaks(text):
    return Markup(text.replace('\n', '<br>'))

# Route for the main page, defaults to Chapter 1
@app.route("/")
@app.route("/chapter/<int:chapter_num>")
def chapter(chapter_num=1):
    # Get the chapter text
    chapter_key = f"Chapter {chapter_num}"
    chapter_text = chapters.get(chapter_key, "Chapter not found.")
    chapter_text = add_html_line_breaks(chapter_text)


    # Determine the availability of next and previous chapters
    next_chapter = chapter_num + 1 if f"Chapter {chapter_num + 1}" in chapters else None
    prev_chapter = chapter_num - 1 if chapter_num > 1 else None

    # Render the chapter text with navigation buttons
    return render_template('chapter.html', text=chapter_text, next_chapter=next_chapter, prev_chapter=prev_chapter)


app.run(debug=True, port=7000)
