import base64
import os
import random
import tempfile
import time
import traceback
from datetime import date
from typing import List, Optional, Any, Tuple
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import tempfile
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from xhtml2pdf import pisa

import utils    

class LinkedInEasyApplier:
    def __init__(self, driver, wait_time: int = 10):
        self.driver = driver
        self.wait_time = wait_time
        self.wait = WebDriverWait(self.driver, self.wait_time)

    def _process_question(self, section) -> None:
        try:
            questions = section.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__question')
            for question in questions:
                self._answer_question(question)
        except NoSuchElementException:
            print("No questions found in this section.")
        except Exception as e:
            print(f"Error processing questions: {str(e)}")

    def _answer_question(self, question) -> None:
        try:
            question_text = question.text.strip()
            print(f"Question: {question_text}")
            answer_elements = question.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__answer')
            for answer_element in answer_elements:
                answer_text = answer_element.text.strip()
                print(f"Answer: {answer_text}")
                if answer_text.lower() == "yes":
                    answer_element.click()
                    print("Answer selected: Yes")
                    break
                elif answer_text.lower() == "no":
                    answer_element.click()
                    print("Answer selected: No")
                    break
        except NoSuchElementException:
            print("No answer options found for this question.")
        except Exception as e:
            print(f"Error answering question: {str(e)}")

    def _scroll_page(self) -> None:
        scrollable_element = self.driver.find_element(By.TAG_NAME, 'html')
        utils.scroll_slow(self.driver, scrollable_element, step=300, reverse=False)
        utils.scroll_slow(self.driver, scrollable_element, step=300, reverse=True)

    def _fill_application_form(self):
        while True:
            self.fill_up()
            if self._next_or_submit():
                break

    def _next_or_submit(self):
        next_button = self.driver.find_element(By.CLASS_NAME, "artdeco-button--primary")
        button_text = next_button.text.lower()
        if 'submit application' in button_text:
            self._unfollow_company()
            time.sleep(random.uniform(1.5, 2.5))
            next_button.click()
            time.sleep(random.uniform(1.5, 2.5))
            return True
        time.sleep(random.uniform(1.5, 2.5))
        next_button.click()
        time.sleep(random.uniform(3.0, 5.0))
        self._check_for_errors()


    def _unfollow_company(self) -> None:
        try:
            form_sections = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
            for section in form_sections:
                self._process_question(section)
        except NoSuchElementException:
            print("No additional questions found.")
        except Exception as e:
            print(f"Error filling additional questions: {str(e)}")

    def _click_apply_button(self) -> None:
        try:
            apply_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="continue_unqualified"]')))
            apply_button.click()
            print("Apply button clicked.")
        except TimeoutException:
            print("Apply button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking apply button: {str(e)}")

    def fill_up(self) -> None:
        try:
            easy_apply_content = self.driver.find_element(By.CLASS_NAME, 'jobs-easy-apply-content')
            pb4_elements = easy_apply_content.find_elements(By.CLASS_NAME, 'pb4')
            for element in pb4_elements:
                self._process_form_element(element)
        except Exception as e:
            pass
        


    def _process_form_element(self, element: WebElement) -> None:
        try:
            next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="continue_applicant"]')))
            next_button.click()
            print("Next button clicked.")
        except TimeoutException:
            print("Next button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking next button: {str(e)}")

    def _click_submit_button(self) -> None:
        try:
            submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="submit_application"]')))
            submit_button.click()
            print("Submit button clicked.")
        except TimeoutException:
            print("Submit button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking submit button: {str(e)}")

    def _handle_upload_fields(self, element: WebElement) -> None:
        file_upload_elements = self.driver.find_elements(By.XPATH, "//input[@type='file']")
        for element in file_upload_elements:
            parent = element.find_element(By.XPATH, "..")
            self.driver.execute_script("arguments[0].classList.remove('hidden')", element)
            if 'resume' in parent.text.lower():
                if self.resume_dir != None:
                    resume_path = self.resume_dir.resolve()
                if self.resume_dir != None and resume_path.exists() and resume_path.is_file():
                    element.send_keys(str(resume_path))
                else:
                    self._create_and_upload_resume(element)
            elif 'cover' in parent.text.lower():
                self._create_and_upload_cover_letter(element)

    def _create_and_upload_resume(self, element):
        max_retries = 3
        retry_delay = 1
        folder_path = 'generated_cv'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for attempt in range(max_retries):
            try:
                html_string = self.gpt_answerer.get_resume_html()
                with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as temp_html_file:
                    temp_html_file.write(html_string)
                    file_name_HTML = temp_html_file.name

                file_name_pdf = f"resume_{uuid.uuid4().hex}.pdf"
                file_path_pdf = os.path.join(folder_path, file_name_pdf)
                
                with open(file_path_pdf, "wb") as f:
                    f.write(base64.b64decode(utils.HTML_to_PDF(file_name_HTML)))
                    
                element.send_keys(os.path.abspath(file_path_pdf))
                time.sleep(2)  # Give some time for the upload process
                os.remove(file_name_HTML)
                return True
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    tb_str = traceback.format_exc()
                    raise Exception(f"Max retries reached. Upload failed: \nTraceback:\n{tb_str}")

    def _upload_resume(self, element: WebElement) -> None:
        element.send_keys(str(self.resume_dir))

    def _create_and_upload_cover_letter(self, element: WebElement) -> None:
        cover_letter = self.gpt_answerer.answer_question_textual_wide_range("Write a cover letter")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
            letter_path = temp_pdf_file.name
            c = canvas.Canvas(letter_path, pagesize=letter)
            width, height = letter
            text_object = c.beginText(100, height - 100)
            text_object.setFont("Helvetica", 12)
            text_object.textLines(cover_letter)
            c.drawText(text_object)
            c.save()
            element.send_keys(letter_path)

    def _fill_additional_questions(self) -> None:
        form_sections = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
        for section in form_sections:
            self._process_question(section)

    def _process_question(self, section: WebElement) -> None:
        if self._handle_terms_of_service(section):
            return
        self._handle_radio_question(section)
        self._handle_textbox_question(section)
        self._handle_date_question(section)
        self._handle_dropdown_question(section)

    def _handle_terms_of_service(self, element: WebElement) -> bool:
        try:
            review_application_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="review_application"]')))
            review_application_button.click()
            print("Review application button clicked.")
        except TimeoutException:
            print("Review application button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking review application button: {str(e)}")

    def _click_close_button(self) -> None:
        try:
            close_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="close_application"]')))
            close_button.click()
            print("Close button clicked.")
        except TimeoutException:
            print("Close button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking close button: {str(e)}")

    def _click_cancel_button(self) -> None:
        try:
            cancel_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="cancel_application"]')))
            cancel_button.click()
            print("Cancel button clicked.")
        except TimeoutException:
            print("Cancel button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking cancel button: {str(e)}")

    def _click_back_button(self) -> None:
        try:
            back_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="back_application"]')))
            back_button.click()
            print("Back button clicked.")
        except TimeoutException:
            print("Back button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking back button: {str(e)}")