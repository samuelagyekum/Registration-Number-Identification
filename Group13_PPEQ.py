#!/usr/bin/env python
# coding: utf-8

# In[ ]:



students = {}
global_count = 0
VOWELS = set("AEIOU")

# Manual accent replacement table
ACCENT_MAP = {
    # French accents
    'À':'A','Á':'A','Â':'A','Ã':'A','Ä':'A','Å':'A','Ā':'A','Ă':'A','Ą':'A',
    'à':'A','á':'A','â':'A','ã':'A','ä':'A','å':'A','ā':'A','ă':'A','ą':'A',
    'Ç':'C','Ć':'C','Ĉ':'C','Ċ':'C','Č':'C','ç':'C','ć':'C','ĉ':'C','ċ':'C','č':'C',
    'È':'E','É':'E','Ê':'E','Ë':'E','Ē':'E','Ĕ':'E','Ė':'E','Ę':'E','Ě':'E',
    'è':'E','é':'E','ê':'E','ë':'E','ē':'E','ĕ':'E','ė':'E','ę':'E','ě':'E',
    'Ì':'I','Í':'I','Î':'I','Ï':'I','Ĩ':'I','Ī':'I','Ĭ':'I','Į':'I','İ':'I',
    'ì':'I','í':'I','î':'I','ï':'I','ĩ':'I','ī':'I','ĭ':'I','į':'I','ı':'I',
    'Ñ':'N','Ń':'N','Ņ':'N','Ň':'N','ñ':'N','ń':'N','ņ':'N','ň':'N',
    'Ò':'O','Ó':'O','Ô':'O','Õ':'O','Ö':'O','Ø':'O','Ō':'O','Ŏ':'O','Ő':'O',
    'ò':'O','ó':'O','ô':'O','õ':'O','ö':'O','ø':'O','ō':'O','ŏ':'O','ő':'O',
    'Œ':'OE','œ':'OE',
    'Ù':'U','Ú':'U','Û':'U','Ü':'U','Ũ':'U','Ū':'U','Ŭ':'U','Ů':'U','Ű':'U','Ų':'U',
    'ù':'U','ú':'U','û':'U','ü':'U','ũ':'U','ū':'U','ŭ':'U','ů':'U','ű':'U','ų':'U',
    'Ý':'Y','ý':'Y','ÿ':'Y','Ÿ':'Y',
    'ß':'SS',
    
    # Spanish accents
    'á':'A','é':'E','í':'I','ó':'O','ú':'U','ü':'U','ñ':'N',
    'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ü':'U','Ñ':'N',
    
    # German accents
    'Ä':'A','Ö':'O','Ü':'U','ä':'A','ö':'O','ü':'U','ß':'SS',
    
    # Scandinavian
    'Å':'A','å':'A','Ø':'O','ø':'O','Æ':'AE','æ':'AE','Ø':'O','ø':'O',
    'Ø':'O','ø':'O',
    'Ø':'O','ø':'O','Ø':'O','ø':'O',
    
    # Eastern European / Slavic
    'Ł':'L','ł':'L','Š':'S','š':'S','Ž':'Z','ž':'Z','Ć':'C','ć':'C','Đ':'D','đ':'D','Ř':'R','ř':'R','Ň':'N','ň':'N'
}


def remove_accents(s):
    """
    Title: Remove Accents from a String

    Description:
        Replace accented letters with their unaccented equivalents using a manual mapping.

    Input:
        s (str): A string potentially containing accented letters.

    Output:
        str: A string with accents replaced by unaccented letters.

    Example:
        remove_accents("Élysée") -> "ELYSEE"
    """
    return "".join(ACCENT_MAP.get(ch, ch) for ch in s)


def is_valid_name_input(s):
    """
    Title: Validate Name Input

    Description:
        Checks if the input string contains only letters, spaces, or hyphens.

    Input:
        s (str): Name string to validate.

    Output:
        bool: True if valid, False otherwise.

    Example:
        is_valid_name_input("Jean-Paul") -> True
        is_valid_name_input("Jean123") -> False
    """
    for c in s:
        if not (c.isalpha() or c in " -"):
            return False
    return True


def normalize_name_for_key(s):
    """
    Title: Normalize Name for Key

    Description:
        Removes accents, converts to uppercase, and removes spaces and hyphens.
        Useful for generating unique keys for student dictionary.

    Input:
        s (str): Name string.

    Output:
        str: Normalized string suitable as a dictionary key.

    Example:
        normalize_name_for_key("Élysée-Champs") -> "ELYSEECHAMPS"
    """
    s = remove_accents(s)
    s = s.upper().replace(" ", "").replace("-", "")
    return s


def extract_consonants(name_norm):
    """
    Title: Extract First 3 Consonants

    Description:
        From a normalized name, extract the first three consonants.
        Pads with 'X' if fewer than three consonants are present.

    Input:
        name_norm (str): Normalized name string.

    Output:
        str: String of 3 consonants.

    Example:
        extract_consonants("SMITH") -> "SMT"
        extract_consonants("AI") -> "IXX"
    """
    consonants = [c for c in name_norm if c not in VOWELS]
    result = "".join(consonants[:3])
    return result.ljust(3, "X")


def extract_letters(name_norm):
    """
    Title: Extract First 3 Letters

    Description:
        Extract the first three letters from a normalized name.
        Pads with 'X' if fewer than three letters are present.

    Input:
        name_norm (str): Normalized name string.

    Output:
        str: String of 3 letters.

    Example:
        extract_letters("John") -> "JOH"
        extract_letters("Al") -> "ALX"
    """
    return name_norm[:3].ljust(3, "X")

def generate_registration_number(last_name, first_name):
    """
    Title: Generate Student Registration Number

    Description:
        Generates a unique student registration number by combining:
        - First 3 consonants of last name
        - First 3 letters of first name
        - Incremental counter (padded to 3 digits)
        Ensures uniqueness across registered students.

    Input:
        last_name (str): Student's last name.
        first_name (str): Student's first name.

    Output:
        str: Registration number (or error message if input invalid).

    Example:
        generate_registration_number("Élysée", "Jean") -> "LYSJEJ001"
    """
    global global_count

    if not (is_valid_name_input(last_name) and is_valid_name_input(first_name)):
        return "Error: Names must contain only letters, spaces, or hyphens."

    last_norm = normalize_name_for_key(last_name)
    first_norm = normalize_name_for_key(first_name)

    key = (last_norm, first_norm)
    if key in students:
        return f"⚠️ Already registered: {students[key]['reg']}"

    field1 = extract_consonants(last_norm)
    field2 = extract_letters(first_norm)

    global_count += 1
    count = str(global_count).rjust(3, "0")

    reg_number = field1 + field2 + count
    students[key] = {'reg': reg_number, 'last': last_name, 'first': first_name}
    return reg_number
    
## Main Execution: Interactive Student Registration 
if __name__ == "__main__":
    while True:
        last = input("Enter last name (or 'quit' to exit): ").strip()
        if last.lower() == "quit":
            break
        first = input("Enter first name: ").strip()
        reg = generate_registration_number(last, first)
        print("Registration number:", reg)

    # Print all registered students
    if students:
        print("\nAll registered students:")
        for v in students.values():
            print(f"{v['last']} {v['first']} -> {v['reg']}")


# In[ ]:




