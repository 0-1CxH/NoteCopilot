# Start


```python
pip install -r requirements.txt
cp services.yaml.sample services.yaml
```

Put your API url and key in the  `services.yaml` file:

```yaml
services:
  # Standard OpenAI API service
  openai:
    type: openai
    api_endpoint: "https://api.openai.com/v1"
    api_key: "your-openai-api-key"
    default_model_name: "default_model_name" # add a default model here

  # Azure OpenAI API services
  azure:
    type: azure
    api_endpoint: "https://your-resource-name.openai.azure.com"
    api_key: "your-azure-api-key"
    api_version: "2024-02-15-preview"
    default_model_name: "default_model_name" # add a default model here

```

Simply run by:

```python
python main.py
```



# Manual

<b>AI Features</b>
    <ul style="margin-top:6px;margin-bottom:6px;">
      <li><b>Completion</b>: Select text or place the cursor, then click the <span class="fas fa-magic"></span> button or press <b>Ctrl+Q</b>. AI will continue or complete your text.</li>
      <li><p><b>Ask Copilot</b>: Select text or place the cursor, then click the <span class="fas fa-brain"></span> button or press <b>Ctrl+Q</b>, enter your query with the help of pre-defined templates. AI will answer your query.</p><p>Note: when entering your query, use <b>Shift+Enter</b> for a new line and <b>Enter</b> for submitting the query.</li></p></li>
    </ul>
<b>Menu Buttons</b>
  <table style="flex:1;font-size:0.98em;border-collapse:collapse;">
            <thead>
              <tr>
                <th style="padding:4px 8px;text-align:left;border-bottom:1px solid #e3e7ed;">Button Description</th>
                <th style="padding:4px 8px;text-align:left;border-bottom:1px solid #e3e7ed;">Keyboard Shortcut</th>
              </tr>
            </thead>
           <tbody>
              <tr><td style="padding:2px 8px;">Completion (AI)</td><td style="padding:2px 8px;"><b>Ctrl+Q</b></td></tr>
              <tr><td style="padding:2px 8px;">Ask Copilot (AI)</td><td style="padding:2px 8px;"><b>Ctrl+W</b></td></tr>
              <tr><td style="padding:2px 8px;">Code Block</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Table</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Table of Content</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Blockquote</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">TODO</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">LaTeX</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Detail</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Bold</td><td style="padding:2px 8px;"><b>Ctrl+B</b></td></tr>
              <tr><td style="padding:2px 8px;">Italic</td><td style="padding:2px 8px;"><b>Ctrl+I</b></td></tr>
              <tr><td style="padding:2px 8px;">Highlight</td><td style="padding:2px 8px;"><b>Ctrl+H</b></td></tr>
              <tr><td style="padding:2px 8px;">Strikethrough</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Underline</td><td style="padding:2px 8px;"><b></b></td></tr>
              <tr><td style="padding:2px 8px;">Load</td><td style="padding:2px 8px;"><b>Ctrl+L</b></td></tr>
              <tr><td style="padding:2px 8px;">Save</td><td style="padding:2px 8px;"><b>Ctrl+S</b></td></tr>
              <tr><td style="padding:2px 8px;">Export Markdown</td><td style="padding:2px 8px;"><b>Ctrl+M</b></td></tr>
              <tr><td style="padding:2px 8px;">Export HTML</td><td style="padding:2px 8px;"><b>Ctrl+N</b></td></tr>
              <tr><td style="padding:2px 8px;">Export PDF</td><td style="padding:2px 8px;"><b></b></td></tr>
            </tbody>
          </table>
<b>Auto Save</b>
        <ul style="margin-top:6px;">
          <li>If current note is loaded or saved already, the <b>CTRL+S</b> will save the note without making you choose a filename, also, it will be automatically saved every 60 seconds.</li>
        </ul>
