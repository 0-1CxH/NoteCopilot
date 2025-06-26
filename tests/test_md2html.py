from src.md2html_convert import Markdown2HTMLConverter

sample_markdown = '''
[TOC]

# Sample Markdown Document with Comprehensive Syntax

This is a **bold** text and this is *italic*. Here's some `inline code`.

## Table of Contents and Navigation
- [Code Examples](#code-examples)
- [Tables](#tables)  
- [Task Lists](#task-lists)
- [Links and References](#links-and-references)

---

## Code Examples {#code-examples}

### Code Block with Syntax Highlighting
```python
def hello_world():
    print("Hello, World!")
    return "success"
# This is a comment
x = [1, 2, 3, 4, 5]
```

### Different Language Examples
```javascript
const greeting = (name) => {
    console.log(`Hello, ${name}!`);
    return true;
};
```

```bash
#!/bin/bash
echo "Running deployment script..."
cd /var/www/html
git pull origin main
```

### Code Block Without Language
```
Plain text code block
No syntax highlighting
Just monospace font
```

## Tables {#tables}

### Basic Table
| Name | Age | City |
|------|-----|------|
| John | 25  | NYC  |
| Jane | 30  | LA   |

### Table with Alignment
| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left         | Center         | Right         |
| Text         | Text           | Text          |
| More data    | More data      | More data     |

### Complex Table
| Feature | Basic | Pro | Enterprise |
|---------|-------|-----|------------|
| Users | 1 | 10 | Unlimited |
| Storage | 1GB | 100GB | 1TB |
| Support | Email | Priority | 24/7 Phone |
| Price | Free | $9.99/mo | $99.99/mo |

## Task Lists {#task-lists}

### TODO Items
- [x] ✅ Completed task
- [x] Another completed item
- [ ] 🔲 Pending task
- [ ] Another pending item
- [x] ~~Crossed out completed task~~
- [ ] Task with **bold** text
- [ ] Task with *italic* text
- [ ] Task with `code` text

### Nested Task Lists
- [x] Main task completed
  - [x] Subtask 1 completed
  - [ ] Subtask 2 pending
  - [x] Subtask 3 completed
- [ ] Another main task
  - [ ] Sub-item A
  - [ ] Sub-item B

## Quote Examples

### Simple Blockquote
> This is a blockquote.
> It can span multiple lines.

### Nested Blockquotes
> This is the first level of quoting.
>
> > This is nested blockquote.
> > 
> > > And this is a third level.
>
> Back to first level.

### Blockquote with Other Elements
> ## This is a header in blockquote
> 
> 1. This is the first list item.
> 2. This is the second list item.
> 
> Here's some code in a blockquote:
> 
>     return shell_exec("echo $input | $markdown_script");

## List Examples

### Unordered Lists
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
    - Deep nested item 2.2.1
    - Deep nested item 2.2.2
- Item 3

### Ordered Lists
1. First item
2. Second item
   1. Nested ordered item
   2. Another nested item
      1. Deep nested item
      2. Another deep nested item
3. Third item

### Mixed Lists
1. Ordered item 1
   - Unordered sub-item
   - Another unordered sub-item
2. Ordered item 2
   1. Ordered sub-item
   - Mixed with unordered
3. Ordered item 3

### Definition Lists
Term 1
:   Definition 1

Term 2
:   Definition 2a
:   Definition 2b

## Images and Files

### Regular Images
![Sample Image](tests/a_picture.png)
![Alt Text](https://via.placeholder.com/300x150/0066CC/FFFFFF?text=Blue+Image)

### Images with Titles
![Sample Image](https://en.wikipedia.org/wiki/Image#/media/File:Image_created_with_a_mobile_phone.png "This is a title")

### Local Files
[Local Text File](tests/a_readable_file.html)
[Binary File](tests/a_binary_file.bin)

### Reference Style Images
![Reference Image][ref-image]

[ref-image]: https://via.placeholder.com/200x100

## Links and References {#links-and-references}

### Regular Links
[Regular Link](https://www.example.com)
[Web Preview](https://www.github.com)

### Automatic Links
<https://www.google.com>
<user@example.com>

### Reference Style Links
This is [a reference link][ref-link] and here's [another one][1].

[ref-link]: https://www.example.com "Optional Title"
[1]: https://www.stackoverflow.com

### Links with Titles
[Link with Title](https://www.example.com "This is a title")

## Advanced Formatting

### Text Formatting
**Bold text** and *italic text* and ***bold italic***.

~~Strikethrough text~~

==Highlighted text==

Subscript: H~2~O and Superscript: x^2^

### Keyboard Keys
Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to copy.
Use <kbd>Cmd</kbd>+<kbd>V</kbd> on Mac.

### Line Breaks
This line ends with two spaces  
And this is a new line.

This line has a manual line break\
Using backslash.

## Horizontal Rules

---

***

___

## Footnotes

This text has a footnote[^1]. Here's another footnote[^note].

[^1]: This is the first footnote.
[^note]: This is a longer footnote with multiple lines.
    
    It can even contain code blocks:
    
        def footnote_example():
            return "footnote"

## Math Equations (if supported)

Inline math: $E = mc^2$

Block math:
$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$

## Emoji Support

:smile: :heart: :thumbsup: :rocket: :tada: :fire:

## HTML Mixed In

This is <em>emphasized</em> using HTML.

<div class="custom-class">
This is a custom HTML div with markdown **bold** text inside.
</div>

<details>
<summary>Click to expand</summary>
<div class="content">
<p>This is hidden content that can be expanded.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
    

</details>

## Code Spans and Escaping

Use `backticks` for code spans.

Here's how to escape characters: \*not italic\* and \`not code\`.

Backslash: \\
Asterisk: \*
Underscore: \_
Curly braces: \{ \}
Square brackets: \[ \]
Parentheses: \( \)
Hash: \#
Plus: \+
Minus: \-
Dot: \.
Exclamation: \!

## Special Characters and Entities

Copyright: &copy; 2024
Trademark: &trade;
Registered: &reg;
Less than: &lt;
Greater than: &gt;
Ampersand: &amp;

## Admonitions/Alerts (if supported)

!!! note
    This is a note admonition.

!!! warning
    This is a warning message.

!!! danger
    This is a danger alert.

## Mermaid Diagrams (if supported)

```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
```

## Headers of All Levels

# H1 Header
## H2 Header  
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

## Complex Example

Here's a complex example combining multiple elements:

> ### Quote with Header
> 
> This blockquote contains:
> 
> 1. **Bold text**
> 2. *Italic text*
> 3. `Code span`
> 4. [A link](https://example.com)
> 5. A footnote[^complex]
> 
> ```python
> # Code block inside blockquote
> def example():
>     return "Hello from blockquote"
> ```
> 
> | Column 1 | Column 2 |
> |----------|----------|
> | Data 1   | Data 2   |
> 
> - [x] Completed task in blockquote
> - [ ] Pending task in blockquote

[^complex]: This footnote is referenced from within a blockquote.

---

*End of comprehensive markdown test document.*

**Total word count:** Approximately 500+ words with comprehensive syntax coverage.
'''

converter = Markdown2HTMLConverter()

# Convert to HTML
html_output = converter(sample_markdown, only_return_body=False)

# Save to file
with open('tests/output.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Conversion complete! Check output.html")
print(f"Sample markdown length: {len(sample_markdown)} characters")
print(f"Generated HTML length: {len(html_output)} characters")