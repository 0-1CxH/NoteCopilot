import markdown
import os

class Markdown2HTMLConverter:
    def __init__(self) -> None:
        self.enabled_extensiosns = [
            'codehilite',
            'fenced_code',
            'tables',
            'toc'
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
        }

        self.executor = markdown.Markdown(
            extensions=self.enabled_extensiosns,
            extension_configs=self.extension_configs
        )

        self.css_content = self.load_css_from_file("static/blocks.css")
    
    def load_css_from_file(self, css_file):
        assert os.path.exists(css_file)
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        return css_content
    
    def __call__(self, text):
        html_content = self.executor.convert(text)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML</title>
    <style>
        {self.css_content}
    </style>
</head>
<body>
    <div class="content">
        {html_content}
    </div>
</body>
</html>"""
        



