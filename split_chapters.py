import re
import os

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '_', value)
    return value

def split_latex_file(input_file, output_dir):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.readlines()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    new_main_content = []
    current_chapter_content = []
    current_chapter_filename = None
    
    # Preamble ends at \begin{document}
    # But we want to keep everything before the first chapter in main.tex
    # Actually, the user wants to split by chapters. 
    # Let's look for \chapter
    
    chapter_pattern = re.compile(r'\\chapter\*?\{(.+?)\}')
    
    # We need to handle the preamble and front matter separately
    # The first chapter starts around line 332
    
    in_preamble = True
    chapter_count = 0
    
    for line in content:
        match = chapter_pattern.match(line.strip())
        if match:
            # If we were collecting a chapter, save it
            if current_chapter_filename:
                with open(os.path.join(output_dir, current_chapter_filename), 'w', encoding='utf-8') as f:
                    f.writelines(current_chapter_content)
                new_main_content.append(f'\\include{{capitulos/{current_chapter_filename[:-4]}}}\n')
                current_chapter_content = []
            
            # Start new chapter
            in_preamble = False
            chapter_title = match.group(1)
            # Handle citations in title if any, remove them for filename
            chapter_title_clean = re.sub(r'\\cite\{.*?\}', '', chapter_title)
            
            chapter_count += 1
            safe_title = slugify(chapter_title_clean)
            if not safe_title:
                safe_title = f"chapter_{chapter_count}"
            
            current_chapter_filename = f"{chapter_count:02d}_{safe_title}.tex"
            current_chapter_content.append(line)
        else:
            if in_preamble:
                new_main_content.append(line)
            else:
                current_chapter_content.append(line)

    # Save the last chapter
    if current_chapter_filename:
        with open(os.path.join(output_dir, current_chapter_filename), 'w', encoding='utf-8') as f:
            f.writelines(current_chapter_content)
        new_main_content.append(f'\\include{{capitulos/{current_chapter_filename[:-4]}}}\n')

    # Write the new main.tex
    # We need to be careful not to overwrite the original immediately, or maybe we do.
    # Let's write to main_refactored.tex first
    with open('main_refactored.tex', 'w', encoding='utf-8') as f:
        f.writelines(new_main_content)

if __name__ == "__main__":
    split_latex_file('main.tex', 'capitulos')
