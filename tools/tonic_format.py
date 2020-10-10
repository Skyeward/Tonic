def format_string(string_to_format: str, make_lowercase: bool = True, remove_special_characters: bool = True, char_replacements: {str: str} = None):
    "Formats a string based on chosen rules. char_replacements will replace the any appearances of keys with their associated value."

    formatted_input = string_to_format
    
    if char_replacements != None:
        for char_to_replace, replacement_char in char_replacements.items():
            if char_to_replace == replacement_char:
                continue

            formatted_input = formatted_input.replace(char_to_replace, replacement_char)
    
    formatted_input = formatted_input.strip()

    formatted_input = formatted_input.replace("'", "")
    formatted_input = formatted_input.replace("--", " ")

    while formatted_input.find("  ") != -1: #removes any spacing larger than a single space
        formatted_input = formatted_input.replace("  ", " ")

    if remove_special_characters == True:
        formatted_input = "".join(char for char in formatted_input if ord(char) > 31 and ord(char) < 126)

    if make_lowercase == True:
        formatted_input = formatted_input.lower()
    
    return formatted_input