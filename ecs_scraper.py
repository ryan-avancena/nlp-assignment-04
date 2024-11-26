import os
import pathlib
import json
import pandas as pd 
import numpy as np

# from bs4 import BeautifulSoup
from requests_html import HTMLSession

cs_catalog_2024 = 'https://catalog.fullerton.edu/preview_program.php?catoid=91&poid=42762&hl=%22Computer+Science%2C+B.S.%22&returnto=search'

session = HTMLSession()

def get_courses(link):

    """
        input: url to CSUF Computer Science 24-25 catalog from California State University, Fullerton
        output: .json file with course catalog
    """

    r = session.get(link)

    # Render JavaScript if necessary
    r.html.render(timeout=20)

    # Locate all sections with the `acalog-core` class
    sections = r.html.find('div.acalog-core')
    
    # 3 = Lower-Division Core (18)
    # 4 = Upper-Division Core (30)
    # 5 = Mathematics Requirements (18)
    # 6 = Science and Math Electives (12)
    # 8 = Computer Science Electives (15)
    # 9 = Graduation Requirement

    course_types = [
        'low_div_core',
        'upper_div_core',
        'math_req',
        'sci_math_elec',
        'cs_electives',
        'grad_req'
    ]

    sections_idx = [2,3,4,5,7,8]

    cs_courses = {}

    if sections:
        # print(f"Found {len(sections)} sections.")
        
        course_type_idx = 0

        for idx, section in enumerate(sections, start=0):
            # extract all course items within the section
            course_items = section.find('li.acalog-course')
            courses = [course.find('a', first=True).text for course in course_items if course.find('a', first=True)]

            if courses and (idx in sections_idx):
                cs_courses[f'{course_types[course_type_idx]}'] = courses
                course_type_idx += 1    
            
        
    return cs_courses


def main():
    cs_courses = get_courses(cs_catalog_2024)
    with open("cs_courses.json", "w") as f:
        json.dump(cs_courses, f, indent=4) 
    print("Saved output to cs_courses.json")

main()
