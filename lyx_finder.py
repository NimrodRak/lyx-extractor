import regex as re

MACRO_PATTERN_STRING = rf"\\begin_inset FormulaMacro[\w\W]*?\\end_inset"
HEBREW_CLAIM = "טענה"
HEBREW_THEOREM = "משפט"
THEOREM_PATTERN_STRING = rf"\\begin_layout Description\n(?:(?:\b{HEBREW_CLAIM}\b)|(?:\b{HEBREW_THEOREM}\b))[\w\W]*?\\end_layout"
HEADER_PATTERN_STRING = rf"^[\w\W]*?\\begin_body"
BEGIN_STANDARD_LAYOUT = "\\begin_layout Standard\n"
END_LAYOUT = "\\end_layout\n"
END_DOCUMENT = "\\end_body\n\\end_document"
NEW_FILE_NAME = "./lanew.lyx"
RAW_FILE_NAME = "./latest.lyx"
NEWLINE = "\n"

def match_content(content, pattern_string):
    pattern = re.compile(pattern_string)
    matches = pattern.findall(content)
    return matches


def main():
    with open(RAW_FILE_NAME, encoding="utf8") as content_file:
        content = content_file.read()
    headers = match_content(content, HEADER_PATTERN_STRING)
    if len(headers) != 1:
        print("Error locating proper header! Exiting...")
        return
    header = headers[0]
    macros = match_content(content, MACRO_PATTERN_STRING)
    theorems = match_content(content, THEOREM_PATTERN_STRING)
    
    with open(NEW_FILE_NAME, "w", encoding="utf8") as new_file:
        new_file.write(header + NEWLINE)
        new_file.write(BEGIN_STANDARD_LAYOUT)
        for macro in macros:
            new_file.write(macro + NEWLINE)
        new_file.write(END_LAYOUT)
        for theorem in theorems:
            BEGIN_LAYOUT_TEXT = "\\begin_layout Enumerate\n"
            BEGIN_LAYOUT_LENGTH = len(r"\begin_layout Description משפט ")
            new_file.write(BEGIN_LAYOUT_TEXT + theorem[BEGIN_LAYOUT_LENGTH:] + NEWLINE)
        new_file.write(END_DOCUMENT)

if __name__ == "__main__":
    main()
