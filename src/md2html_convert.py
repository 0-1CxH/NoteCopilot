import markdown
import os
from bs4 import BeautifulSoup

class Markdown2HTMLConverter:
    def __init__(self) -> None:
        self.enabled_extensiosns = [
            'admonition',                # Admonitions/Alerts
            'pymdownx.details',          # Collapsible admonitions
            'pymdownx.superfences',      # SuperFences for custom code blocks (e.g., mermaid)
            'codehilite',
            'fenced_code',
            'tables',
            'toc',
            'pymdownx.tilde',      # ~~strikethrough~~ and ~subscript~
            'pymdownx.mark',       # ==highlight==
            'pymdownx.caret',      # ^superscript^
            'pymdownx.tasklist',   # [x] task lists
            'pymdownx.arithmatex', # $math$ and $$math$$
            # 'footnotes', 'smarty', 'attr_list', 'wikilinks'
        ]
        self.extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': False, 
                'linenos': True,
                'linenostart': 1,
            },
            'pymdownx.tasklist': {
                'custom_checkbox': True,
            },
            'pymdownx.arithmatex': {
                'generic': True,
            },
            'pymdownx.superfences': {
                'custom_fences': [
                    {
                        'name': 'mermaid',
                        'class': 'mermaid',
                        'format': '!!python/name:pymdownx.superfences.fence_code_format',
                    },
                ],
            },
        }

        self.executor = markdown.Markdown(
            extensions=self.enabled_extensiosns,
            extension_configs=self.extension_configs
        )

        self.css_content = self.load_content_from_file("static/blocks.css")
        self.js_content = self.load_content_from_file("static/blocks.js")
    
    def load_content_from_file(self, css_file):
        assert os.path.exists(css_file)
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        return css_content
    
    def __call__(self, text):
        html_content = self.executor.convert(text)
        self.executor.reset()
        html_content = self.post_process_html(html_content)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML</title>
    <style>
        {self.css_content}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <div class="content">
        {html_content}
    </div>
    <script>
    {self.js_content}
    </script>
</body>
</html>"""
    
    def post_process_html(self, html_content):
        """Post-process the HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Process tables: add 'markdown-table' class to non-code tables
        for table in soup.find_all('table'):
            # Skip tables that are for code highlighting (e.g., class 'highlighttable')
            if 'highlighttable' in table.get('class', []):
                continue
            # Check if this table is part of a code block
            parent = table.parent
            is_code_table = False
            while parent:
                parent_classes = parent.get('class', [])
                if (
                    (parent.name == 'div' and 'highlight' in parent_classes) or
                    (parent.name == 'table' and 'highlighttable' in parent_classes)
                ):
                    is_code_table = True
                    break
                parent = parent.parent
            # Add class to non-code tables
            if not is_code_table:
                current_classes = table.get('class', [])
                if 'markdown-table' not in current_classes:
                    current_classes.append('markdown-table')
                table['class'] = current_classes
        
        # 2. Process hyperlinks
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue

            # Determine link type and add appropriate class
            if href.startswith('#'):
                # In-page anchor link
                link['class'] = link.get('class', []) + ['jump-link']
            elif href.startswith(('http://', 'https://', 'ftp://', 'sftp://', 'mailto:')):
                # Web URL
                link['class'] = link.get('class', []) + ['web-url']
            else:
                # Local file path
                link['class'] = link.get('class', []) + ['file-path']
        
        # 3. process mark class
        # Convert "mark" tag to "markdown-hlt"
        # Convert all <mark> tags to <markdown-hlt> tags
        for mark in soup.find_all('mark'):
            new_tag = soup.new_tag('markdown-hlt')
            # Move all children from <mark> to <markdown-hlt>
            for child in mark.contents:
                new_tag.append(child)
            mark.replace_with(new_tag)
        

        
        return str(soup)
        



