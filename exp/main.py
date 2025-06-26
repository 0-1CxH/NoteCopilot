from flask import Flask, render_template_string, request, jsonify
from src.md2html_convert import Markdown2HTMLConverter

app = Flask(__name__)


# Initialize converter
converter = Markdown2HTMLConverter()
