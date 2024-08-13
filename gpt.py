import json
import os
import re
import textwrap
from datetime import datetime
from typing import Dict, List

from dotenv import load_dotenv
from langchain_core.messages.ai import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.prompts import ChatPromptTemplate
from Levenshtein import distance
import requests

import strings

load_dotenv()

# Update for Gemini API 
from langchain.chains import LLMChain, ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMLogger:
    
    def __init__(self, llm):
        self.llm = llm

    def log(self, prompt, response):
        log_entry = {
            "model": self.llm.model_name,
            "time": datetime.now().isoformat(),
            "prompts": [prompt],
            "replies": [response],
            "total_tokens": 2048,
            "input_tokens": 2048,
            "output_tokens": 2048,
            "total_cost": 0.0
        }

        with open("calls_log.json", "a", encoding="utf-8") as f:
            json_string = json.dumps(log_entry, ensure_ascii=False, indent=4)
            f.write(json_string + "\n")

    @staticmethod
    def log_request(prompts, parsed_reply: Dict[str, Dict]):
        calls_log = os.path.join(os.getcwd(), "gemini_calls.json")
        if isinstance(prompts, StringPromptValue):
            prompts = prompts.text
        elif isinstance(prompts, Dict):
            prompts = {
                f"prompt_{i+1}": prompt.content
                for i, prompt in enumerate(prompts.messages)
            }
        else:
            prompts = {
                f"prompt_{i+1}": prompt.content
                for i, prompt in enumerate(prompts.messages)
            }

        current_time = datetime.now().isoformat()

        token_usage = parsed_reply["token_usage"]
        output_tokens = token_usage["output_tokens"]
        input_tokens = token_usage["input_tokens"]
        total_tokens = token_usage["total_tokens"]

        model_name = parsed_reply["model"]

        prompt_price_per_token = 0.00000015
        completion_price_per_token = 0.0000006

        total_cost = (input_tokens * prompt_price_per_token) + (
            output_tokens * completion_price_per_token
        )

        log_entry = {
            "model": model_name,
            "time": current_time,
            "prompts": prompts,
            "replies": parsed_reply["content"],
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": total_cost,
        }

        with open(calls_log, "a", encoding="utf-8") as f:
            json_string = json.dumps(log_entry, ensure_ascii=False, indent=4)
            f.write(json_string + "\n")

   # ... (rest of the class implementation remains the same)

class LoggerChatModel:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm


    def __call__(self, messages: List[Dict[str, str]]) -> str:
        reply = self.llm(messages)
        parsed_reply = self.parse_llmresult(reply)
        LLMLogger.log_request(prompts=messages, parsed_reply=parsed_reply)
        return reply

    def parse_llmresult(self, llmresult: str) -> Dict[str, Dict]:
        return {
            "content": llmresult['content'],
            "response_metadata": {"model_name": llmresult['model']},
            "id": llmresult['id'],
            "usage_metadata": {
                "input_tokens": llmresult['token_usage']['input_tokens'],
                "output_tokens": llmresult['token_usage']['output_tokens'],
                "total_tokens": llmresult['token_usage']['total_tokens'],
            },
        }


class GPTAnswerer:
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key
        self.llm_cheap = LoggerChatModel(
            ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=self.gemini_api_key, temperature=0.3)
        )
        self.llm_gemini = self.llm_cheap

    @property 
    def job_description(self):
        return self.job.description

    @staticmethod
    def find_best_match(text: str, options: list[str]) -> str:
        distances = [
            (option, distance(text.lower(), option.lower())) for option in options
        ]
        best_option = min(distances, key=lambda x: x[1])[0]
        return best_option

    @staticmethod
    def _remove_placeholders(text: str) -> str:
        text = text.replace("PLACEHOLDER", "")
        return text.strip()

    @staticmethod
    def _preprocess_template_string(template: str) -> str:
        return textwrap.dedent(template)

    def set_resume(self, resume):
        self.resume = resume

    def set_job(self, job):
        self.job = job
        self.job.set_summarize_job_description(
            self.summarize_job_description(self.job.description)
        )

    def summarize_job_description(self, text: str) -> str:
        strings.summarize_prompt_template = self._preprocess_template_string(
            strings.summarize_prompt_template
        )
        prompt = ChatPromptTemplate.from_template(strings.summarize_prompt_template)
        chain = LLMChain(llm=self.llm_cheap, prompt=prompt, output_parser=StrOutputParser())
        output = chain.run({"text": text})
        return output
    
    def get_resume_html(self):
        resume_markdown_prompt = ChatPromptTemplate.from_template(strings.resume_markdown_template)
        fusion_job_description_resume_prompt = ChatPromptTemplate.from_template(strings.fusion_job_description_resume_template)
        resume_markdown_chain = LLMChain(llm=self.llm_cheap, prompt=resume_markdown_prompt, output_parser=StrOutputParser())
        fusion_job_description_resume_chain = LLMChain(llm=self.llm_cheap, prompt=fusion_job_description_resume_prompt, output_parser=StrOutputParser())
        
        casual_markdown_path = os.path.abspath("resume_template/casual_markdown.js")
        reorganize_header_path = os.path.abspath("resume_template/reorganizeHeader.js")
        resume_css_path = os.path.abspath("resume_template/resume.css")

        html_template = strings.html_template.format(casual_markdown=casual_markdown_path, reorganize_header=reorganize_header_path, resume_css=resume_css_path)
        composed_chain = (
            resume_markdown_chain
            | (lambda output: {"job_description": self.job.summarize_job_description, "formatted_resume": output})
            | fusion_job_description_resume_chain
            | (lambda formatted_resume: html_template + formatted_resume)
        )
        try:
            output = composed_chain.run({
                "resume": self.resume,
                "job_description": self.job.summarize_job_description
            })
            return output
        except Exception as e:
            pass
        
    def _create_chain(self, template: str):
        prompt = ChatPromptTemplate.from_template(template)
        return LLMChain(llm=self.llm_cheap, prompt=prompt, output_parser=StrOutputParser())

    def answer_question_textual_wide_range(self, question: str) -> str:
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
        chain = LLMChain(llm=self.llm_cheap, prompt=prompt, output_parser=StrOutputParser())
        output = chain.run({"question": question})
        section_name = output.lower().replace(" ", "_")
        if section_name == "cover_letter":
            chain = chains.get(section_name)
            output= chain.run({"resume": self.resume, "job_description": self.job_description})
            return output
        resume_section = getattr(self.resume, section_name, None)
        if resume_section is None:
            raise ValueError(f"Section '{section_name}' not found in the resume.")
        chain = chains.get(section_name)
        if chain is None:
            raise ValueError(f"Chain not defined for section '{section_name}'")
        return chain.run({"resume_section": resume_section, "question": question})

    def answer_question_textual(self, question: str) -> str:
        template = self._preprocess_template_string(strings.resume_stuff_template)
        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=self.llm_cheap, prompt=prompt, output_parser=StrOutputParser())
        output = chain.run({"resume": self.resume, "question": question})
        return output

    def answer_question_numeric(self, question: str, default_experience: int = 3) -> int:
        func_template = self._preprocess_template_string(strings.numeric_question_template)
        prompt = ChatPromptTemplate.from_template(func_template)
        chain = LLMChain(llm=self.llm_cheap, prompt=prompt, output_parser=StrOutputParser())
        output_str = chain.run({"resume": self.resume, "question": question, "default_experience": default_experience})
        try:
            output = self.extract_number_from_string(output_str)
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
        chain = LLMChain(llm=self.llm_cheap, prompt=prompt, output_parser=StrOutputParser())
        output_str = chain.run({"resume": self.resume, "question": question, "options": options})
        best_option = self.find_best_match(output_str, options)
        return best_option

    def try_fix_answer(self, question: str, answer: str, error_text: str) -> str:
        error_text = error_text.lower()
        if error_text == "this is a required field":
            return "Please enter a value"
        elif error_text == "please enter a valid phone number":
            return "123-456-7890"
        elif error_text == "this should be a valid email address":
            return "test@example.com"
        elif "must be at least 5 characters" in error_text:
            if len(answer) > 4:
                return answer
            else:
                return answer + "123"
        elif "must be at least 8 characters" in error_text:
            if len(answer) > 7:
                return answer
            else:
                return answer + "12345"
        else:
            return answer

from langchain_core.language_models import BaseChatModel
import requests

class CustomGeminiModel(BaseChatModel):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def _call(self, messages, stop=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "contents": [{"parts": [{"text": m.content}]} for m in messages]
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    @property
    def _llm_type(self):
        return "custom_gemini"

# Replace GoogleGemini with CustomGeminiModel in your code
# self.llm_cheap = LoggerChatModel(CustomGeminiModel(api_key=gemini_api_key))
