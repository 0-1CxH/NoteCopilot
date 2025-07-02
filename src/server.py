from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from .md2html_convert import Markdown2HTMLConverter
from .ai_copilot import AICopilot
from .stream_reformat import StreamReformatter
import os
import time
import logging

# Set up a basic logger for the server
logger = logging.getLogger("NoteCopilotServer")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

class NoteCopilotServer:
    def __init__(self, static_folder, notes_folder, ai_services_config_path, ai_functions_config_path):
        # Convert relative path to absolute path
        self.static_folder = os.path.abspath(static_folder)
        self.notes_folder = os.path.abspath(notes_folder)
        self.ai_services_config_path = os.path.abspath(ai_services_config_path)
        self.ai_functions_config_path = os.path.abspath(ai_functions_config_path)
        self.app = Flask(__name__, 
                        static_url_path='/static',  # Changed this
                        static_folder=self.static_folder)
        CORS(self.app)
        self.converter = Markdown2HTMLConverter()
        self.copilot = AICopilot(self.ai_services_config_path, self.ai_functions_config_path)
        self.setup_routes()

    def setup_routes(self):
        # Convert markdown endpoint
        self.app.route('/convert', methods=['POST'])(self.convert_markdown)
        # Serve editor endpoint
        self.app.route('/')(self.serve_editor)
        # Serve static files
        self.app.route('/static/<path:path>')(self.serve_static)
        # List markdown files endpoint
        self.app.route('/list')(self.list_md_files)
        # AI mock endpoint
        self.app.route('/ai', methods=['POST'])(self.ai_request)
        # Save markdown file endpoint
        self.app.route('/save', methods=['POST'])(self.save_md_file)
        # Load markdown file endpoint
        self.app.route('/load')(self.load_md_file)
        # Get function cards endpoint
        self.app.route('/funcs')(self.get_funcs)

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

    def list_md_files(self):
        try:
            files = [f[:-3] for f in os.listdir(self.notes_folder) if f.endswith('.md')]
            return jsonify({'files': files})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def ai_request(self):
        data = request.get_json()
        resp_stream = self.copilot(data)
        return Response(StreamReformatter.execute(resp_stream), mimetype='text/plain')
        # return Response(resp_stream, mimetype='text/plain')

    def save_md_file(self):
        data = request.get_json()
        if not data or 'filename' not in data or 'content' not in data:
            return jsonify({'error': 'Missing name or content field'}), 400
        name = data['filename'] + '.md'
        content = data['content']
        # Prevent directory traversal
        if '/' in name or '\\' in name or name.startswith('.'):
            return jsonify({'error': 'Invalid file name'}), 400
        file_path = os.path.join(self.notes_folder, name)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def load_md_file(self):
        filename = request.args.get('file') + '.md'
        if not filename or '/' in filename or '\\' in filename or filename.startswith('.'):
            return jsonify({'error': 'Invalid file name'}), 400
        file_path = os.path.join(self.notes_folder, filename)
        if not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'content': content})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_funcs(self):
        return jsonify({'funcs': self.copilot.get_funcs(return_json=True)})

    def run(self, debug, port):
        self.app.run(debug=debug, port=port)