import re
import sys

MACRO_PATTERN_STRING = rf"\\begin_inset FormulaMacro[\w\W]*?\\end_inset"
HEBREW_CLAIM = "טענה"
HEBREW_THEOREM = "משפט"
HEBREW_COROLLARY = "מסקנה"
HEBREW_DEFINTION = "הגדרה"
HEADER_PATTERN_STRING = rf"^[\w\W]*?\\begin_body"
BEGIN_STANDARD_LAYOUT = "\\begin_layout Standard\n"
END_LAYOUT = "\\end_layout\n"
BEGIN_LAYOUT_TEXT = "\\begin_layout Enumerate\n"
BEGIN_LAYOUT_LENGTH = len(r"\begin_layout Description") + 1
END_DOCUMENT = "\\end_body\n\\end_document"
NEW_FILE_NAME ="./new.lyx"
RAW_FILE_NAME = "./raw.lyx"
NEWLINE = "\n"
generate_key_concat = lambda lst: "(?:" + "|".join([rf"(?:\b{x}\b)" for x in lst]) + ")"
# hlp = re.compile(r"\\begin_inset ERT(?:.*?)hyper(?:\w*?)\{link\d+\}\{(\w+)\}\n\\end_layout", re.DOTALL)
# "\\begin_inset ERT(?:.*?)\{link(?:\d*?)\}\{([\w\W]*?)\}(?:.*?)end_inset"
# hlp = re.compile(r"\\begin_inset ERT\nstatus open\n\n\\begin_layout Plain Layout\n\n\n\\backslash\nhyper\w{,6}\{link(?:\d{,2})\}\{(.*?)\}\n\\end_layout\n\n\\end_inset", re.DOTALL)

hlp = re.compile(
    r'(\\begin_inset ERT(?:[\s\S]{,200}?)\{link(?:\d*?)\}\{([\w\W]*?)\}(?:[\s\S]*?)\\end_inset)')
def match_content(content, pattern_string):
    pattern = re.compile(pattern_string)
    matches = pattern.findall(content)
    # the following lines dont match porperly
    return matches


def main():
    if len(sys.argv) != 2 or any([c not in ('d', 't') for c in sys.argv[1]]):
        print("please have exactly on arg and be 'd' or 't'")
        return
    with open(RAW_FILE_NAME, encoding="utf8") as content_file:
        content = content_file.read()
    headers = match_content(content, HEADER_PATTERN_STRING)
    if len(headers) != 1:
        print("Error locating proper header! Exiting...")
        return
    
    header = headers[0]
    macros = match_content(content, MACRO_PATTERN_STRING)
    keys_list = []
    if 'd' in sys.argv[1]:
        keys_list.extend([HEBREW_DEFINTION])
    if 't' in sys.argv[1]: 
        keys_list.extend([HEBREW_CLAIM, HEBREW_COROLLARY, HEBREW_THEOREM])
    theorem_pattern = rf"\\begin_layout Description\n{generate_key_concat(keys_list)}[\w\W]*?\\end_layout"
    content = hlp.sub(r"\2", content)
    theorems = match_content(content, theorem_pattern)
    
    with open(NEW_FILE_NAME, "w", encoding="utf8") as new_file:
        new_file.write(header + NEWLINE)
        new_file.write(BEGIN_STANDARD_LAYOUT)
        for macro in macros:
            new_file.write(macro + NEWLINE)
        new_file.write(END_LAYOUT)
        for theorem in theorems:
            new_file.write(BEGIN_LAYOUT_TEXT + theorem[BEGIN_LAYOUT_LENGTH + theorem[BEGIN_LAYOUT_LENGTH:].find(" ") + 1:] + NEWLINE)
        new_file.write(END_DOCUMENT)


if __name__ == "__main__":
    main()
