
def sanitize_weka(text: str, remove_newlines=True, escape_doublequote=True, escape_singlequote=True,remove_separator=None) -> str:
    
    if remove_newlines:
        text = text.replace('\n', ' ') 
    if escape_doublequote:
        text = text.replace('"', '')
    if escape_singlequote:
        text = text.replace("'", "") 
    if remove_separator: 
        text = text.replace(remove_separator," ")
    return text
