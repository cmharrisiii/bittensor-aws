def generate_toc_prompt(topic):
    prompt = (f"Generate a detailed and structured Table of Contents for a comprehensive report about '{topic}'. "
              f"The Table of Contents should cover all important aspects and subtopics related to '{topic}', "
              f"and should follow this structure: major sections are numbered as integers (1, 2, 3, etc.), "
              f"and subsections under each major section are numbered as 'major.minor' (1.1, 1.2, etc.). "
              f"The final section should be 'Conclusion' with no subsections. "
              f"Don't respond with anything other than the Structured Table of Contents. So the first line should start with 1 "
              f"and don't add any other any other information after the table of contents either. "
              f"Please ensure each major section and subsection starts with a number and is appropriately titled.")
    return prompt
