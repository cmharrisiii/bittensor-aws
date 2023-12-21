import re

def toc_prompt_creation(topic, toc_response):
    """
    After receiving the table of contents from the initial prompt and validating the
    initial response, we need to break them out into a prompt for each subsection of each section. 

    params: 
        topic str: the topic that the table of contents is about
        toc_response str: the response from the initial prompt

    returns:
        prompts list(str): a list of prompts for each subsection of each section
    """


    # Strip leading/trailing white space and split into lines
    lines = toc_response.strip().split("\n")

    # Regex pattern to match lines that are either sections or subsections
    pattern = re.compile(r'([A-Za-z\- ]+|\d+\.\d+ [A-Za-z\- ]+)')
    actual_toc_ls = []

    prompts = []

    # Loop through the response
    for line in lines:
        match = pattern.search(line.strip())
        if match:
            current_section = match.group(0).strip()
            actual_toc_ls.append(line.strip())
            # print(f"line: {current_section}\nline[0]: {current_section[0]} is_numeric: {current_section[0].isnumeric()}\n")
            if not current_section[0].isnumeric():  # If this is a major section
                print(current_section)
                if "introduction" in current_section.lower():
                    prompts.append(f"Please write a 1 or 2 paragraph general introduction to the document on the topic {topic}")
                elif "conclusion" in current_section.lower():
                    prompts.append(f"Please write a 1 or 2 paragraph conclusion to the document on the topic {topic}")
                else:
                    prompts.append(f"Please write a 1 or 2 paragraph introduction to the section '{current_section}' in the context of the {topic} document.")
            else:  # This is a subsection
                prompts.append(f"Please expand on the topic '{topic}' with 1 or 2 paragraphs in the context of the section '{current_section}' and the broader {topic} document.")

    # Output the prompts
    for prompt in prompts:
        print(prompt)

    return prompts, actual_toc_ls


if __name__ == '__main__':
    topic = 'War of 1812'
    response = """1. Introduction
2. Causes of the War
   2.1 Economic Factors
   2.2 Impressment of American Sailors
   2.3 British Support for Native American Tribes
   2.4 American Expansionism
3. Declaration and Outbreak of War
   3.1 War Hawks in Congress
   3.2 President Madison's Call for War
   3.3 Initial Military Campaigns
4. Naval Battles and Blockades
   4.1 USS Constitution vs. HMS Guerriere
   4.2 Battle of Lake Erie
   4.3 Chesapeake Bay Campaign
   4.4 British Blockade of American Ports
5. Land Campaigns
   5.1 Invasion of Upper Canada
   5.2 Defense of Lower Canada
   5.3 Battle of New Orleans
   5.4 Creek War and Andrew Jackson
6. Native American Involvement
   6.1 Tecumseh and the Confederacy
   6.2 Battle of Tippecanoe
   6.3 Native American Allies on the British Side
   6.4 Effects on Native American Tribes
7. British Burning of Washington, D.C.
   7.1 Capture of Washington, D.C.
   7.2 Destruction of Public Buildings
   7.3 Significance of the Event
8. Treaty of Ghent
   8.1 Negotiations and Terms
   8.2 Impact on Border Issues
   8.3 Resumption of Pre-War Relations
9. Legacy and Significance
   9.1 Impact on National Identity
   9.2 Relationship with Canada
   9.3 Influence on Future Conflicts
10. Conclusion
"""
    print(toc_prompt_creation(topic, response))