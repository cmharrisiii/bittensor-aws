import re

def validate_toc(response):
    """
    Validate the table of contents response from the initial prompt.

    We're expecting the response to have more than 6 valid lines, where a valid line is defined as:
        - a major section (e.g. 1. Introduction)
        - a subsection (e.g. 1.1. Background) and up to 4 levels of subsections (e.g. 1.1.2.3.4 History)

    params:
        response str: the response from the initial prompt

    returns:
        validated bool: whether the response is valid or not
        cleaned_response: the response with all invalid lines removed
    """

    lines = response.split('\n')
    
    major_section_re = re.compile(r'^\d+\. [A-Za-z0-9\-\s]+$')
    subsection_re = re.compile(r'^\s*\d+\.\d+ [A-Za-z0-9\-\s]+$')
    sub_subsection_re = re.compile(r'^\s*\d+\.\d+[\.\d+]{0,6} [A-Za-z0-9\-\s]+$')
    valid_lines = []
    for line in lines:
        if major_section_re.match(line) or subsection_re.match(line) or sub_subsection_re.match(line):
            valid_lines.append(line)
            continue

        if line == '':
            continue

        else:
            print(f"Invalid line: {line}")
            
    if len(valid_lines) < 6:
        print("Not enough valid lines")
        return False, None

    return True, '\n'.join(valid_lines)