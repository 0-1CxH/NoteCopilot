from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from md2html_convert import Markdown2HTMLConverter

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for local development

converter = Markdown2HTMLConverter()

@app.route('/convert', methods=['POST'])
def convert_markdown():
    data = request.get_json()
    if not data or 'markdown' not in data:
        return jsonify({'error': 'Missing markdown field'}), 400
    markdown_text = data['markdown']
    html = converter(markdown_text, only_return_body=False)
    return jsonify({'html': html})

@app.route('/')
def serve_editor():
    return send_from_directory('../static', 'editor.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000) 