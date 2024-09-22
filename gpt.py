import os
import re
from typing import Dict, List

from google.api_core import retry
from google.cloud import aiplatform
from langchain_community.chat_models import ChatGooglePalm, ChatPromptTemplate, StrOutputParser  # Import from langchain-community
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

import google.generativeai as genai  # Added import for genai


class LLMLogger:

    def __init__(self, llm):
        self.llm = llm

    def __call__(self, prompts, stop=None, **kwargs):
        parsed_reply = self.log_request(prompts, self.llm(prompts, stop, **kwargs))
        return parsed_reply

    @staticmethod
    def log_request(prompts, parsed_reply: Dict[str, Dict]):
        print("-" * 40)
        print(f"PROMPT: {prompts}")
        print(f"REPLY: {parsed_reply}")
        print("-" * 40)
        return parsed_reply


class GPTAnswerer:
    def __init__(self, openai_api_key: str, google_api_key: str):
        self.openai_api_key = openai_api_key
        self.google_api_key = google_api_key  # Ensure the API key is used as a string, not as a file path

    # Example adjustment: If previously you were opening the API key as a file, remove that.
    # For instance, change from:
    # with open(google_api_key, 'r') as key_file:
    #     self.google_api_key = key_file.read().strip()
    # To:
    # self.google_api_key = google_api_key

    def _query_gemini(self, prompts):
        response = genai.generate_content(prompt=prompts[0].content)
        return {'output': {'output': response['text']}}

    @staticmethod
    def find_best_match(text: str, options: list[str]) -> str:
        similarity_scores = [
            (option, self._calculate_similarity(text.lower(), option.lower())) for option in options
        ]
        best_match = max(similarity_scores, key=lambda x: x[1])[0]
        return best_match

    @staticmethod
    def _remove_placeholders(text: str) -> str:
        text = text.replace("PLACEHOLDER", "")
        return text.strip()

    @staticmethod
    def _preprocess_template_string(template: str) -> str:
        # Preprocess a template string to remove unnecessary indentation.
        return template.strip()

    def set_resume(self, resume):
        self.resume = resume

    def summarize_job_description(self, text: str) -> str:
        template = self._preprocess_template_string(strings.summarize_prompt_template)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke({"text": text})
        return output['text']
    

    def get_resume_html(self):
        resume_markdown_prompt = ChatPromptTemplate.from_template(strings.resume_markdown_template)
        fusion_job_description_resume_prompt = ChatPromptTemplate.from_template(strings.fusion_job_description_resume_template)
        resume_markdown_chain = resume_markdown_prompt | self.llm_cheap | StrOutputParser()
        fusion_job_description_resume_chain = fusion_job_description_resume_prompt | self.llm_cheap | StrOutputParser()
        
        casual_markdown_path = os.path.abspath("resume_template/casual_markdown.js")
        reorganize_header_path = os.path.abspath("resume_template/reorganizeHeader.js")
        resume_css_path = os.path.abspath("resume_template/resume.css")

        html_template = strings.html_template.format(casual_markdown=casual_markdown_path, reorganize_header=reorganize_header_path, resume_css=resume_css_path)
        composed_chain = (
            resume_markdown_chain
            | (lambda output: {"job_description": self.summarize_job_description, "formatted_resume": output})
            | fusion_job_description_resume_chain
            | (lambda formatted_resume: html_template + formatted_resume)
        )
        try:
            output = composed_chain.invoke({
                "resume": self.resume,
                "job_description": self.summarize_job_description(self.resume)
            })
            return output['text']
        except Exception as e:
            print(f"Error during elaboration: {e}")
            return None
        

    def _create_chain(self, template: str):
        prompt = ChatPromptTemplate.from_template(template)
        return prompt | self.llm_cheap | StrOutputParser()

    def answer_question_textual_wide_range(self, question: str) -> str:
        # Define chains for each section of the resume
        chains = {
            "personal_information": self._create_chain(strings.personal_information_template),
            "self_identification": self._create_chain(strings.self_identification_template),
            "legal_authorization": self._create_chain(strings.legal_authorization_template),
            "work_preferences": self._create_chain(strings.work_preferences_template),
            "education_details": self._create_chain(strings.education_details_template),
            "experience_details": self._create_chain(strings.experience_details_template),
            "projects": self._create_chain(strings.projects_template),
            "availability": self._create_chain(strings.availability_template),
            "salary_expectations": self._create_chain(strings.salary_expectations_template),
            "certifications": self._create_chain(strings.certifications_template),
            "languages": self._create_chain(strings.languages_template),
            "interests": self._create_chain(strings.interests_template),
            "cover_letter": self._create_chain(strings.coverletter_template),
        }
        section_prompt = (
            f"For the following question: '{question}', which section of the resume is relevant? "
            "Respond with one of the following: Personal information, Self Identification, Legal Authorization, "
            "Work Preferences, Education Details, Experience Details, Projects, Availability, Salary Expectations, "
            "Certifications, Languages, Interests, Cover letter"
        )
        prompt = ChatPromptTemplate.from_template(section_prompt)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke({"question": question})
        section_name = output.lower().replace(" ", "_")
        if section_name == "cover_letter":
            chain = chains.get(section_name)
            output= chain.invoke({"resume": self.resume, "job_description": self.job_description})
            return output
        resume_section = getattr(self.resume, section_name, None)
        if resume_section is None:
            raise ValueError(f"Section '{section_name}' not found in the resume.")
        chain = chains.get(section_name)
        if chain is None:
            raise ValueError(f"Chain not defined for section '{section_name}'")
        return chain.invoke({"resume_section": resume_section, "question": question})

    def answer_question_textual(self, question: str) -> str:
        template = self._preprocess_template_string(strings.resume_stuff_template)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke({"resume": self.resume, "question": question})
        return output['text']

    def answer_question_numeric(self, question: str, default_experience: int = 3) -> int:
        func_template = self._preprocess_template_string(strings.numeric_question_template)
        prompt = ChatPromptTemplate.from_template(func_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output_str = chain.invoke({"resume": self.resume, "question": question, "default_experience": default_experience})
        try:
            output = self.extract_number_from_string(output_str['text'])
        except ValueError:
            output = default_experience
        return output

    def extract_number_from_string(self, output_str):
        numbers = re.findall(r"\d+", output_str)
        if numbers:
            return int(numbers[0])
        else:
            raise ValueError("No numbers found in the string")

    def answer_question_from_options(self, question: str, options: list[str]) -> str:
        func_template = self._preprocess_template_string(strings.options_template)
        prompt = ChatPromptTemplate.from_template(func_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output_str = chain.invoke({"resume": self.resume, "question": question, "options": options})
        best_option = self.find_best_match(output_str['text'], options)
        return best_option

