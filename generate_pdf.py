import markdown
import os
import re

def assemble_book_from_sidebar(sidebar_path, output_md_path):
    """
    Reads _sidebar.md to get the chapter order, reads those files,
    and combines them into a single book.md file.
    """
    if not os.path.exists(sidebar_path):
        print(f"Sidebar file not found: {sidebar_path}")
        return

    print("Assembling book from sidebar...")
    
    # 1. Extract file paths from sidebar
    chapter_files = []
    with open(sidebar_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Find links like [Title](path/to/file.md)
        chapter_files = re.findall(r'\[.*?\]\((.*?)\)', content)

    # 2. Start with Title and Cover Image
    full_book_content = "# Atreya Mahakavya\n\n![](atrya-mahakavya-book.png)\n\n"

    # 3. Append each chapter
    for rel_path in chapter_files:
        file_path = rel_path.replace('/', os.sep)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as cf:
                text = cf.read()
                # Fix relative image paths (../images -> images) if necessary
                text = text.replace("](..", "](") 
                full_book_content += f"\n\n{text}\n\n---\n"
                print(f"Added: {file_path}")
        else:
            print(f"Warning: Chapter file missing: {file_path}")

    # 4. Save to book.md
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(full_book_content)
    print(f"Book assembly complete: {output_md_path}")


if __name__ == "__main__":
    assemble_book_from_sidebar("_sidebar.md", "book.md")