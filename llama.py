import requests
from dotenv import load_dotenv
import os 
import json

load_dotenv()

api_token = os.getenv("HF_API_TOKEN")
if not api_token:
    raise ValueError("API token is not set")

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	print(response.json())
	return response.json()
	
def load_courses(filename):
    with open(filename, "r") as f:
        return json.load(f)

def answer_question(courses, question):
    lower_question = question.lower()
    
    if "upper division" in lower_question:
        context = "These are the upper division courses:\n" + "\n".join(courses.get("upper_div_core", []))
    elif "lower division" in lower_question:
        context = "These are the lower division courses:\n" + "\n".join(courses.get("low_div_core", []))
    elif "math requirements" in lower_question:
        context = "These are the math requirement courses:\n" + "\n".join(courses.get("math_req", []))
    else:
        context = "I couldn't find a specific category for your question. Here's an overview of all courses:\n\n"
        for category, course_list in courses.items():
            context += f"{category}:\n" + "\n".join(f"- {course}" for course in course_list) + "\n\n"

    # query Llama API with the context
    output = query({"inputs": f"{context}\n\nQuestion: {question}\nAnswer:"})

    if output:
        return output[0]["generated_text"].strip()
    else:
        return "Sorry, I couldn't process the request."

def main():
    courses = load_courses("cs_courses.json")
    question = input("Ask a question about the courses: ")
    answer = answer_question(courses, question)
    print("\nAnswer:")
    print(answer)

if __name__ == "__main__":
    main()