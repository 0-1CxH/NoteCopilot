import markdown
import os
import re
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

        self.css_content = f'''
<style>
    {self.load_content_from_file("static/md-blocks.css")}
</style>
'''
        self.js_content_before_body = f'''
<script>
    {self.load_content_from_file("static/latex-math.js")}
</script>'''
        self.js_content_after_body = f'''
<script>
    {self.load_content_from_file("static/copy-btn.js")}
</script>
        '''
    
    def load_content_from_file(self, css_file):
        assert os.path.exists(css_file)
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        return css_content
    
    def __call__(self, text, only_return_body):
        # First, separate ai-message segments from regular markdown content
        segments = self.separate_ai_message_segments(text)
        
        # Process each segment
        processed_segments = []
        for segment_type, segment_content in segments:
            if segment_type == 'ai-message':
                # Process ai-message segment separately
                processed_html = self.process_ai_message_segment(segment_content)
                processed_segments.append(processed_html)
            else:
                # Process regular markdown content
                html_content = self.executor.convert(segment_content)
                self.executor.reset()
                html_content = self.post_process_html(html_content)
                processed_segments.append(html_content)
        
        # Concatenate all processed segments
        final_html_content = ''.join(processed_segments)

        if only_return_body:
            return final_html_content
        else:
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML</title>
    {self.css_content}
    {self.js_content_before_body}
</head>
<body>
    <div class="content">
        {final_html_content}
    </div>
</body>
    {self.js_content_after_body}
</html>"""
    
    def separate_ai_message_segments(self, text):
        """Separate ai-message segments from regular markdown content"""
        segments = []
        current_pos = 0
        
        # Pattern to match ai-message blocks
        # This matches <ai-message>...</ai-message> with any content inside
        ai_message_pattern = r'<ai-message>(.*?)</ai-message>'
        
        for match in re.finditer(ai_message_pattern, text, re.DOTALL):
            # Add any content before the ai-message
            if match.start() > current_pos:
                regular_content = text[current_pos:match.start()]
                if regular_content.strip():
                    segments.append(('regular', regular_content))
            
            # Add the ai-message content
            ai_message_content = match.group(1)
            segments.append(('ai-message', ai_message_content))
            
            current_pos = match.end()
        
        # Add any remaining content after the last ai-message
        if current_pos < len(text):
            remaining_content = text[current_pos:]
            if remaining_content.strip():
                segments.append(('regular', remaining_content))
        
        return segments
    
    def process_ai_message_segment(self, ai_message_content):
        """Process an ai-message segment, handling its internal components"""
        # Create the outer ai-message tag
        soup = BeautifulSoup('<ai-message></ai-message>', 'html.parser')
        ai_message_tag = soup.find('ai-message')
        
        # Find think and response components
        think_match = re.search(r'<ai-message-component-think>(.*?)</ai-message-component-think>', 
                               ai_message_content, re.DOTALL)
        response_match = re.search(r'<ai-message-component-response>(.*?)</ai-message-component-response>', 
                                  ai_message_content, re.DOTALL)
        
        if think_match:
            think_content = think_match.group(1).strip()
            # Convert markdown content to HTML
            think_html = self.executor.convert(think_content)
            self.executor.reset()
            
            # Create think component
            think_tag = soup.new_tag('ai-message-component-think')
            think_tag.append(BeautifulSoup(think_html, 'html.parser'))
            # Add original content as data attribute for copy functionality
            think_tag['data-original-content'] = think_content
            ai_message_tag.append(think_tag)
        
        if response_match:
            response_content = response_match.group(1).strip()
            # Convert markdown content to HTML
            response_html = self.executor.convert(response_content)
            self.executor.reset()
            
            # Create response component
            response_tag = soup.new_tag('ai-message-component-response')
            response_tag.append(BeautifulSoup(response_html, 'html.parser'))
            # Add original content as data attribute for copy functionality
            response_tag['data-original-content'] = response_content
            ai_message_tag.append(response_tag)
        
        return str(soup)
    
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
        



