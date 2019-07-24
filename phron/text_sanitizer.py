
def sanitize_weka(text: str) -> str:
    text = text.replace('\n', ' ')
    text = text.replace('"', "\\\"")
    text = text.replace("'", "\\\'")
    return text