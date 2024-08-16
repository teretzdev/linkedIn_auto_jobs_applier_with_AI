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

    def _click_continue_button(self) -> None:
        try:
            continue_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="continue_application"]')))
            continue_button.click()
            print("Continue button clicked.")
        except TimeoutException:
            print("Continue button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking continue button: {str(e)}")

    def _click_save_button(self) -> None:
        try:
            save_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="save_application"]')))
            save_button.click()
            print("Save button clicked.")
        except TimeoutException:
            print("Save button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking save button: {str(e)}")

    def _click_discard_button(self) -> None:
        try:
            discard_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="discard_application"]')))
            discard_button.click()
            print("Discard button clicked.")
        except TimeoutException:
            print("Discard button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking discard button: {str(e)}")

    def _click_edit_button(self) -> None:
        try:
            edit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="edit_application"]')))
            edit_button.click()
            print("Edit button clicked.")
        except TimeoutException:
            print("Edit button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking edit button: {str(e)}")

    def _click_delete_button(self) -> None:
        try:
            delete_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="delete_application"]')))
            delete_button.click()
            print("Delete button clicked.")
        except TimeoutException:
            print("Delete button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking delete button: {str(e)}")

    def _click_view_button(self) -> None:
        try:
            view_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="view_application"]')))
            view_button.click()
            print("View button clicked.")
        except TimeoutException:
            print("View button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking view button: {str(e)}")

    def _click_share_button(self) -> None:
        try:
            share_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="share_application"]')))
            share_button.click()
            print("Share button clicked.")
        except TimeoutException:
            print("Share button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking share button: {str(e)}")

    def _click_print_button(self) -> None:
        try:
            print_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="print_application"]')))
            print_button.click()
            print("Print button clicked.")
        except TimeoutException:
            print("Print button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking print button: {str(e)}")

    def _click_download_button(self) -> None:
        try:
            download_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="download_application"]')))
            download_button.click()
            print("Download button clicked.")
        except TimeoutException:
            print("Download button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking download button: {str(e)}")

    def _click_copy_button(self) -> None:
        try:
            copy_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="copy_application"]')))
            copy_button.click()
            print("Copy button clicked.")
        except TimeoutException:
            print("Copy button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking copy button: {str(e)}")

    def _click_remove_button(self) -> None:
        try:
            remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="remove_application"]')))
            remove_button.click()
            print("Remove button clicked.")
        except TimeoutException:
            print("Remove button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking remove button: {str(e)}")

    def _click_add_button(self) -> None:
        try:
            add_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="add_application"]')))
            add_button.click()
            print("Add button clicked.")
        except TimeoutException:
            print("Add button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking add button: {str(e)}")

    def _click_upload_button(self) -> None:
        try:
            upload_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="upload_application"]')))
            upload_button.click()
            print("Upload button clicked.")
        except TimeoutException:
            print("Upload button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking upload button: {str(e)}")

    def _click_download_all_button(self) -> None:
        try:
            download_all_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="download_all_applications"]')))
            download_all_button.click()
            print("Download all button clicked.")
        except TimeoutException:
            print("Download all button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking download all button: {str(e)}")

    def _click_delete_all_button(self) -> None:
        try:
            delete_all_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="delete_all_applications"]')))
            delete_all_button.click()
            print("Delete all button clicked.")
        except TimeoutException:
            print("Delete all button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking delete all button: {str(e)}")

    def _click_clear_all_button(self) -> None:
        try:
            clear_all_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="clear_all_applications"]')))
            clear_all_button.click()
            print("Clear all button clicked.")
        except TimeoutException:
            print("Clear all button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking clear all button: {str(e)}")

    def _click_refresh_button(self) -> None:
        try:
            refresh_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="refresh_applications"]')))
            refresh_button.click()
            print("Refresh button clicked.")
        except TimeoutException:
            print("Refresh button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking refresh button: {str(e)}")

    def _click_sort_button(self) -> None:
        try:
            sort_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="sort_applications"]')))
            sort_button.click()
            print("Sort button clicked.")
        except TimeoutException:
            print("Sort button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking sort button: {str(e)}")

    def _click_filter_button(self) -> None:
        try:
            filter_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="filter_applications"]')))
            filter_button.click()
            print("Filter button clicked.")
        except TimeoutException:
            print("Filter button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking filter button: {str(e)}")

    def _click_search_button(self) -> None:
        try:
            search_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="search_applications"]')))
            search_button.click()
            print("Search button clicked.")
        except TimeoutException:
            print("Search button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking search button: {str(e)}")

    def _click_settings_button(self) -> None:
        try:
            settings_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="settings_applications"]')))
            settings_button.click()
            print("Settings button clicked.")
        except TimeoutException:
            print("Settings button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking settings button: {str(e)}")

    def _click_help_button(self) -> None:
        try:
            help_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="help_applications"]')))
            help_button.click()
            print("Help button clicked.")
        except TimeoutException:
            print("Help button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking help button: {str(e)}")

    def _click_about_button(self) -> None:
        try:
            about_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="about_applications"]')))
            about_button.click()
            print("About button clicked.")
        except TimeoutException:
            print("About button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking about button: {str(e)}")

    def _click_feedback_button(self) -> None:
        try:
            feedback_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="feedback_applications"]')))
            feedback_button.click()
            print("Feedback button clicked.")
        except TimeoutException:
            print("Feedback button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking feedback button: {str(e)}")

    def _click_contact_button(self) -> None:
        try:
            contact_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="contact_applications"]')))
            contact_button.click()
            print("Contact button clicked.")
        except TimeoutException:
            print("Contact button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking contact button: {str(e)}")

    def _click_privacy_button(self) -> None:
        try:
            privacy_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="privacy_applications"]')))
            privacy_button.click()
            print("Privacy button clicked.")
        except TimeoutException:
            print("Privacy button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking privacy button: {str(e)}")

    def _click_terms_button(self) -> None:
        try:
            terms_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="terms_applications"]')))
            terms_button.click()
            print("Terms button clicked.")
        except TimeoutException:
            print("Terms button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking terms button: {str(e)}")

    def _click_license_button(self) -> None:
        try:
            license_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="license_applications"]')))
            license_button.click()
            print("License button clicked.")
        except TimeoutException:
            print("License button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking license button: {str(e)}")

    def _click_copyright_button(self) -> None:
        try:
            copyright_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="copyright_applications"]')))
            copyright_button.click()
            print("Copyright button clicked.")
        except TimeoutException:
            print("Copyright button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking copyright button: {str(e)}")

    def _click_trademark_button(self) -> None:
        try:
            trademark_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="trademark_applications"]')))
            trademark_button.click()
            print("Trademark button clicked.")
        except TimeoutException:
            print("Trademark button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking trademark button: {str(e)}")

    def _click_patent_button(self) -> None:
        try:
            patent_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="patent_applications"]')))
            patent_button.click()
            print("Patent button clicked.")
        except TimeoutException:
            print("Patent button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking patent button: {str(e)}")

    def _click_design_button(self) -> None:
        try:
            design_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="design_applications"]')))
            design_button.click()
            print("Design button clicked.")
        except TimeoutException:
            print("Design button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking design button: {str(e)}")

    def _click_utility_button(self) -> None:
        try:
            utility_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="utility_applications"]')))
            utility_button.click()
            print("Utility button clicked.")
        except TimeoutException:
            print("Utility button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking utility button: {str(e)}")

    def _click_plant_button(self) -> None:
        try:
            plant_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="plant_applications"]')))
            plant_button.click()
            print("Plant button clicked.")
        except TimeoutException:
            print("Plant button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking plant button: {str(e)}")

    def _click_animal_button(self) -> None:
        try:
            animal_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="animal_applications"]')))
            animal_button.click()
            print("Animal button clicked.")
        except TimeoutException:
            print("Animal button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking animal button: {str(e)}")

    def _click_microorganism_button(self) -> None:
        try:
            microorganism_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="microorganism_applications"]')))
            microorganism_button.click()
            print("Microorganism button clicked.")
        except TimeoutException:
            print("Microorganism button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking microorganism button: {str(e)}")

    def _click_process_button(self) -> None:
        try:
            process_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="process_applications"]')))
            process_button.click()
            print("Process button clicked.")
        except TimeoutException:
            print("Process button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking process button: {str(e)}")

    def _click_machine_button(self) -> None:
        try:
            machine_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="machine_applications"]')))
            machine_button.click()
            print("Machine button clicked.")
        except TimeoutException:
            print("Machine button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking machine button: {str(e)}")

    def _click_manufacture_button(self) -> None:
        try:
            manufacture_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="manufacture_applications"]')))
            manufacture_button.click()
            print("Manufacture button clicked.")
        except TimeoutException:
            print("Manufacture button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking manufacture button: {str(e)}")

    def _click_composition_button(self) -> None:
        try:
            composition_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="composition_applications"]')))
            composition_button.click()
            print("Composition button clicked.")
        except TimeoutException:
            print("Composition button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking composition button: {str(e)}")

    def _click_article_button(self) -> None:
        try:
            article_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="article_applications"]')))
            article_button.click()
            print("Article button clicked.")
        except TimeoutException:
            print("Article button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking article button: {str(e)}")

    def _click_method_button(self) -> None:
        try:
            method_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="method_applications"]')))
            method_button.click()
            print("Method button clicked.")
        except TimeoutException:
            print("Method button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking method button: {str(e)}")

    def _click_system_button(self) -> None:
        try:
            system_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="system_applications"]')))
            system_button.click()
            print("System button clicked.")
        except TimeoutException:
            print("System button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking system button: {str(e)}")

    def _click_device_button(self) -> None:
        try:
            device_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="device_applications"]')))
            device_button.click()
            print("Device button clicked.")
        except TimeoutException:
            print("Device button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking device button: {str(e)}")

    def _click_software_button(self) -> None:
        try:
            software_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="software_applications"]')))
            software_button.click()
            print("Software button clicked.")
        except TimeoutException:
            print("Software button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking software button: {str(e)}")

    def _click_business_method_button(self) -> None:
        try:
            business_method_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="business_method_applications"]')))
            business_method_button.click()
            print("Business method button clicked.")
        except TimeoutException:
            print("Business method button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking business method button: {str(e)}")

    def _click_data_structure_button(self) -> None:
        try:
            data_structure_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="data_structure_applications"]')))
            data_structure_button.click()
            print("Data structure button clicked.")
        except TimeoutException:
            print("Data structure button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking data structure button: {str(e)}")

    def _click_algorithm_button(self) -> None:
        try:
            algorithm_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="algorithm_applications"]')))
            algorithm_button.click()
            print("Algorithm button clicked.")
        except TimeoutException:
            print("Algorithm button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking algorithm button: {str(e)}")

    def _click_interface_button(self) -> None:
        try:
            interface_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="interface_applications"]')))
            interface_button.click()
            print("Interface button clicked.")
        except TimeoutException:
            print("Interface button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking interface button: {str(e)}")

    def _click_component_button(self) -> None:
        try:
            component_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="component_applications"]')))
            component_button.click()
            print("Component button clicked.")
        except TimeoutException:
            print("Component button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking component button: {str(e)}")

    def _click_system_button(self) -> None:
        try:
            system_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="system_applications"]')))
            system_button.click()
            print("System button clicked.")
        except TimeoutException:
            print("System button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking system button: {str(e)}")

    def _click_process_button(self) -> None:
        try:
            process_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="process_applications"]')))
            process_button.click()
            print("Process button clicked.")
        except TimeoutException:
            print("Process button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking process button: {str(e)}")

    def _click_method_button(self) -> None:
        try:
            method_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="method_applications"]')))
            method_button.click()
            print("Method button clicked.")
        except TimeoutException:
            print("Method button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking method button: {str(e)}")

    def _click_system_button(self) -> None:
        try:
            system_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="system_applications"]')))
            system_button.click()
            print("System button clicked.")
        except TimeoutException:
            print("System button not found or not clickable.")
        except Exception as e:
            print(f"Error clicking system button: {str(e)}")

    def _click_process_button(self) -> None:
        try:
            process_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-control-name="process_applications"]')))
            process_button.click()
            print("Process button clicked.")
        except TimeoutException:
            print("Process button not found