def _fill_additional_questions(self) -> None:
    form_sections = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
    for section in form_sections:
        # Check if the section is the "projects" section
        if "projects" in section.text.lower():
            continue  # Skip processing this section
        self._process_question(section)
