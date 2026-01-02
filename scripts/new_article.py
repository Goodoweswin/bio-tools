import os
import argparse
from datetime import datetime

# Configuration
TEMPLATE_PATH = 'src/_template.html'
OUTPUT_BASE_DIR = 'src/knowledge'

def create_article(title, category, filename):
    # 1. Read Template
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {TEMPLATE_PATH}")
        return

    # 2. Prepare Data
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 3. Replace Placeholders
    content = template_content.replace('{{ title }}', title)
    content = content.replace('{{ category }}', category)
    content = content.replace('{{ date }}', date_str)

    # 4. Determine Output Path
    # Create category directory if it doesn't exist
    category_slug = category.lower().replace(' ', '-')
    output_dir = os.path.join(OUTPUT_BASE_DIR, category_slug)
    os.makedirs(output_dir, exist_ok=True)

    # Ensure filename ends with .html
    if not filename.endswith('.html'):
        filename += '.html'
    
    output_path = os.path.join(output_dir, filename)

    # 5. Write File
    if os.path.exists(output_path):
        print(f"Warning: File {output_path} already exists. Aborting to prevent overwrite.")
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Success! Created new article at: {output_path}")
    print(f"Don't forget to add a link to this article in src/knowledge.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a new knowledge base article from template.')
    parser.add_argument('title', help='Title of the article')
    parser.add_argument('--category', '-c', default='General', help='Category (e.g., AI-Single-Cell, Skin-Aging)')
    parser.add_argument('--filename', '-f', help='Filename (optional, defaults to title-slug)')

    args = parser.parse_args()

    # Auto-generate filename if not provided
    if not args.filename:
        args.filename = args.title.lower().replace(' ', '-').replace('/', '-') + '.html'

    create_article(args.title, args.category, args.filename)
