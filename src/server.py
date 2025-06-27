from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .md2html_convert import Markdown2HTMLConverter
import os

class NoteCopilotServer:
    def __init__(self, static_folder):
        # Convert relative path to absolute path
        self.static_folder = os.path.abspath(static_folder)
        self.app = Flask(__name__, 
                        static_url_path='/static',  # Changed this
                        static_folder=self.static_folder)
        CORS(self.app)
        self.converter = Markdown2HTMLConverter()
        self.setup_routes()

    def setup_routes(self):
        # Convert markdown endpoint
        self.app.route('/convert', methods=['POST'])(self.convert_markdown)
        # Serve editor endpoint
        self.app.route('/')(self.serve_editor)
        # Serve static files
        self.app.route('/static/<path:path>')(self.serve_static)

    def convert_markdown(self):
        data = request.get_json()
        if not data or 'markdown' not in data:
            return jsonify({'error': 'Missing markdown field'}), 400
        markdown_text = data['markdown']
        html = self.converter(markdown_text, only_return_body=False)
        return jsonify({'html': html})

    def serve_editor(self):
        return send_from_directory(self.static_folder, 'editor.html')

    def serve_static(self, path):
        return send_from_directory(self.static_folder, path)

    def run(self, debug, port):
        self.app.run(debug=debug, port=port)