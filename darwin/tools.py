def clean_whitespace(string: str) -> str:
    string = string.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    string = string.strip()

    string = ' '.join(string.split())

    return string
