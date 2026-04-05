def extract_title(markdown):
    lines = markdown.split('\n')

    lines = map(str.strip, lines)

    for line in lines:
        if line.startswith("# "):
            return line.split("# ", 1)[1]

    raise Exception("No heading found")

