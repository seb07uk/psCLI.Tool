#!/usr/bin/env python3
"""
Konwertuj Markdown do PDF
"""
import markdown
from weasyprint import HTML, CSS
import os

# Ścieżki
input_file = "Batch_Scripts_Complete_Collection.md"
output_file = "Batch_Scripts_Collection.pdf"

# Przeczytaj plik Markdown
with open(input_file, 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Konwertuj Markdown na HTML
html_content = markdown.markdown(
    markdown_content,
    extensions=['toc', 'tables', 'codehilite', 'fenced_code']
)

# Dodaj CSS styling
css_styling = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    h1 {
        color: #1a1a1a;
        border-bottom: 3px solid #0066cc;
        padding-bottom: 10px;
        margin-top: 30px;
        font-size: 2em;
    }
    
    h2 {
        color: #0066cc;
        margin-top: 25px;
        font-size: 1.5em;
    }
    
    h3 {
        color: #0099ff;
        margin-top: 20px;
        font-size: 1.2em;
    }
    
    code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    pre {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        border-left: 4px solid #0066cc;
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
        line-height: 1.4;
    }
    
    table {
        border-collapse: collapse;
        margin: 20px 0;
        width: 100%;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    
    th {
        background-color: #0066cc;
        color: white;
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    blockquote {
        border-left: 4px solid #0066cc;
        padding-left: 15px;
        color: #666;
        margin: 20px 0;
    }
    
    a {
        color: #0066cc;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    strong {
        color: #d32f2f;
        font-weight: bold;
    }
    
    ul, ol {
        margin: 15px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 8px 0;
    }
    
    hr {
        border: none;
        border-top: 2px solid #0066cc;
        margin: 30px 0;
    }
    
    .toc {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    page-break-after: auto;
    
    @page {
        margin: 2cm;
        @bottom-center {
            content: counter(page);
        }
    }
</style>
"""

# Stwórz pełny HTML
full_html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Complete Batch Script Collection</title>
    {css_styling}
</head>
<body>
    {html_content}
</body>
</html>
"""

# Konwertuj na PDF
print(f"Konwertowanie {input_file} na PDF...")
HTML(string=full_html).write_pdf(output_file)
print(f"✅ PDF stworzony: {output_file}")
print(f"📊 Rozmiar: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
