from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from typing import List

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

    def fill_additional_questions(self) -> None:
        try:
            form_sections = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
            for section in form_sections:
                # Check if the section is the "projects" section
                if "projects" in section.text.lower():
                    print("Skipping 'projects' section.")
                    continue  # Skip processing this section
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

    def _click_next_button(self) -> None:
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

    def _click_review_application_button(self) -> None:
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
