
def Summarize_Agent(text, handler):
    """
    Use OpenAI's GPT-4 to summarize the text.
    
    Args:
        text (str): The text to summarize.
        
    Returns:
        str: The summarized text.
    """
    
    # try:
    output = handler("Assume you are a doctor, please summarize these medical article into a paragraph, only keep key message, mainly focus on the phenotype and related disease.", 
                     text)
    if 'not a medical-related page' in output.lower():
        return ""
    else:
        return output
    # except:
    #     raise Exception("Error in summarizing the text.")

# @retry(max_attempts=3, delay=1, backoff=2)
def Check_Agent(patient_info, diagnosis_to_judge, disease_knowledge, handler, similar_case_detailed):
    """
    Use OpenAI's GPT-4 to judge the correctness of the diagnosis.

    Args:
        patient_info (dict): The information of the patient.
        diagnosis_to_judge (str): The diagnosis to judge.
        disease_knowledge (str): The knowledge of the disease.
    
    Returns:
        bool: The judgement of the diagnosis.
    """
    # try:
    output = handler.get_completion(
    "Assume you are a doctor specialized in rare disease diagnosis. \
    Based on the patient information, similar case diagnoses, and disease knowledge, evaluate whether the proposed diagnosis is correct for this patient.",
    f"""Begin with a clear "DIAGNOSIS ASSESSMENT: [Correct/Incorrect]" statement, followed by your reasoning.

Structure your analysis as follows:

**PROPOSED DIAGNOSIS ANALYSIS:** Critically evaluate the proposed diagnosis (**{diagnosis_to_judge}**) in relation to the patient's presentation. Highlight points of concordance or discordance. Reference specific findings from similar cases and medical literature that support or contradict the diagnosis.
**REFERENCES:** 
   - List directly relevant evidence from the provided medical literature, webpages and similar cases that specifically supports your assessment.
   - For each reference, provide:
     - A numbered list ([1], [2], etc.)
     - A brief description of the evidence (e.g., article title, summary of finding, or similar case number/summary)
     - The source (e.g., URL, similar case number, or literature excerpt as available)
   - **Each reference should be clearly cited with a [X] in your reasoning above.**
   - Avoid including references that are not directly used in your analysis.

**Example Format:**

DIAGNOSIS ASSESSMENT: [Correct/Incorrect]

**PROPOSED DIAGNOSIS ANALYSIS:**
[Analysis with in-text citations, e.g., "...as seen in Similar Case #2 [2] and supported by Article X [1]..."]

**REFERENCES:**
[1] "Title of Article" – URL: https://...
[2] Similar Case #2: Brief description and diagnosis
[3] Key finding from medical literature excerpt

---

**Patient phenotype:**
{patient_info}

**Similar cases:**
{similar_case_detailed}

**Medical literature:**
{disease_knowledge}

**Diagnosis to judge**
{diagnosis_to_judge}
""")
    if 'incorrect' in output.lower():
        return False, output
    else:
        return True, output

    

# @retry(max_attempts=3, delay=1, backoff=2)
def Check_Patient_Agent(patient_info, retrieved_patient_case, handler):
    """
    Use OpenAI's GPT-4 to judge if two patients case are similar.
    
    Args:
        patient_info (str): The information of the patient.
        retrieved_patient_case (str): The information of the retrieved patient case.
        
    Returns:
        bool: The judgement of the similarity.
    """
    output = handler.get_completion("Assume you are a doctor experienced in rare disease diagnosis, \
                                    please judge if the two patient cases are likely to be the same disease based on the patient information. \
                                    Please only output 'Yes' or 'No'",
                                        "Patient 1 phenotype: " + patient_info + '\n' +
                                        "Patient 2 phenotype: " + retrieved_patient_case
                                        )
    if 'yes' in output.lower():
        return True
    else:
        return False


def Interaction_Agent(patient_info, primary_diagnosis, handler):
    """
    Use OpenAI's GPT-4 to interact with the patient. First, judge if need to ask the patient for more important phenotype.
    If True, return True and a list of phenotype keywords to ask about.
    If False, return False and an empty list.
    
    Args:
        patient_info (str): The information of the patient.
        primary_diagnosis (str): The primary diagnosis.
        handler: The OpenAI handler.
        
    Returns:
        bool: The judgement of whether more information is needed.
        list: A list of phenotype keywords to inquire about.
    """
    output = handler.get_completion(
        "You are a medical specialist in rare disease diagnosis. Review the patient information and primary diagnosis provided.",
        "Task: Determine if there are important phenotypes or symptoms that should be inquired about to confirm or refine the diagnosis.\n\n"
        "If no additional information is needed, respond with exactly: 'NO_ADDITIONAL_PHENOTYPES_NEEDED'\n\n"
        "If additional information is needed, respond with a list of specific phenotype keywords to inquire about, "
        "one per line, without numbering or bullets. Format each keyword as a medical phenotype term without explanation.\n\n"
        "Example response if information is needed:\n"
        "Polycystic kidney dysplasia\n"
        "Neck muscle weakness\n"
        "Thick eyebrow\n"
        "Natal tooth"
        "Patient information: " + patient_info + '\n' +
        "Primary diagnosis: " + primary_diagnosis
    )
    
    if 'NO_ADDITIONAL_PHENOTYPES_NEEDED' in output:
        return False, []
    else:
        # Split the output by line and strip whitespace to get clean keywords
        phenotype_keywords = [keyword.strip() for keyword in output.split('\n') if keyword.strip()]
        return True, phenotype_keywords
    
def quick_check_agent(phenotype_keywords, remaining_phenotype, handler):
    """
    Use OpenAI's GPT-4o mini to quickly find the phenotype from the remaining phenotype.
    
    Args:
        phenotype_keywords (str): The keywords of the phenotype.
        remaining_phenotype (str): The remaining phenotype.
        
    Returns:
        list: A list of phenotypes from the remaining phenotype.
    """
    output = handler(
        "You are a medical specialist in rare diseases.",
        "Roughly Matching phenotypes from the remaining list based on the keywords provided."
        "Format: One phenotype per line, no numbering or bullets."
        "If no matches found, respond with: NO_PHENOTYPES_FOUND\n\n"
        "Keywords: " + ', '.join(phenotype_keywords) + '\n' +
        "Remaining phenotypes: " + ', '.join(remaining_phenotype)
    )

    phenotype_keywords = [keyword.strip() for keyword in output.split('\n') if keyword.strip()]

    return [] if 'NO_PHENOTYPES_FOUND' in output else phenotype_keywords
        
        
