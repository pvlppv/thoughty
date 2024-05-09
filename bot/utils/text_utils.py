import re

feeling_data = {
    "Любовь": "🟣",
    "Радость": "🟢",
    "Грусть": "🔵",
    "Страх": "🟡",
    "Гнев": "🔴",
}


def validate_text(text: str) -> bool:
    """
    Function to validate user text input
    """
    # Check if the text is empty
    if not text:
        return False
    
    # Check if the text has URLs using regex
    if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
        return False
    
    # Check if the text contains excessive whitespace
    # if re.search(r'\s{10,}', text):
    #     return False
    
    # Check if the text contains excessive punctuation marks
    # if len(re.findall(r'[!?.,;:]', text)) > 10:  # Adjust the threshold as needed
    #     return False
    
    # Check if the text contains any HTML-like tags
    if re.search(r'<.*?>', text):
        return False
    
    # Check if the text contains potentially harmful SQL commands
    sql_command_pattern = re.compile(
        r'\b(?:'
        r'DROP\s+(?:DATABASE|SCHEMA)\s+[^\s;]+(?:\s+CASCADE)?|'
        r'DELETE\s+FROM\s+[^\s;]+|'
        r'UPDATE\s+[^\s;]+\s+SET\s+[^\s;]+|'
        r'INSERT\s+INTO\s+[^\s;]+\s+(?:VALUES\s*\(|SELECT\s|UPDATE\s|DELETE\s|INSERT\s+INTO\s+|\s+UNION\s+)|'
        r'ALTER\s+TABLE\s+[^\s;]+\s+(?:DROP\s+COLUMN|ADD\s+COLUMN)|'
        r'CREATE\s+(?:TABLE|INDEX|VIEW|PROCEDURE|FUNCTION|DATABASE|SCHEMA|TRIGGER)'
        r')\b', 
        re.IGNORECASE
    )
    if sql_command_pattern.search(text):
        return False

    # If all checks pass, the text is valid
    return True


def modify_text_ending(text: str) -> str:
    """
    Modifies the text endings in accordance with the Russian language rules.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text.
    """
    # List of common word endings and their variants
    endings = [
        ('а', 'у'),
        ('ая', 'ую'),
        ('я', 'ю'),
    ]

    # Iterate over each ending
    for old_ending, new_ending in endings:
        # Create a regex pattern to match the old ending at the end of a word
        pattern = re.compile(rf'(\b\w*?){re.escape(old_ending)}\b', re.IGNORECASE)
        # Replace occurrences of the old ending with the new ending
        text = pattern.sub(fr'\1{new_ending}', text)

    # Handle special case for modifying adjectives to match feminine gender
    text = re.sub(r'(\b\w*?)ая\b', r'\1ую', text)

    return text
