import sys

script, encoding, error = sys.argv

def main(language_file, encoding, errors):
    line = language_file.readline()
    if line:
        print_line(line, encoding, errors)
        return main(language_file, encoding, errors)


def print_line(line, encoding, error_type):
    next_lang = line.strip()
    raw_bytes = next_lang.encode(encoding, errors=error_type)
    cooked_string = raw_bytes.decode(encoding, errors=error_type)

    print(raw_bytes, "<===>", cooked_string)


languages = open("text/languages.txt", encoding="utf-8")

main(languages, encoding, error)
