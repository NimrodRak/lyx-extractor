import regex as re

MACRO_PATTERN_STRING = rf"\\begin_inset FormulaMacro[\w\W]*?\\end_inset"
THEOREM_PATTERN_STRING = r"\\begin_layout Description\n\b\{}\b[\w\W]*?\\end_layout".format("משפט")
HEADER_PATTERN_STRING = rf"^[\w\W]*?\\begin_body"

def main():
    with open("./raw.txt", encoding="utf8") as content_file:
        content = content_file.read()
    
    header_pattern = re.compile(HEADER_PATTERN_STRING)
    theorem_pattern = re.compile(THEOREM_PATTERN_STRING)
    macro_pattern = re.compile(MACRO_PATTERN_STRING)
    matches = theorem_pattern.findall(content) 
    header = header_pattern.search(content)
    macros = macro_pattern.findall(content)

    if header is None:
        print("Error locating header! Exiting...")
        return

    with open("./new.lyx", "w", encoding="utf8") as new_file:
        new_file.write(header.group() + "\n")
        new_file.write("\\begin_layout Standard\n")
        for macro in macros:
            new_file.write(macro + "\n")
        new_file.write("\\end_layout\n")
        for match in matches:
            new_file.write(match + "\n")
        new_file.write("\\end_body\n\\end_document")

if __name__ == "__main__":
    main()