import markdown
import sys

def markdown_to_html(markdown_file, html_file):
    # Read the Markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Create a minimal HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown to HTML</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 4px;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.md output.html")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    markdown_to_html(markdown_file, html_file)
    print(f"Conversion complete. HTML file saved as {html_file}")