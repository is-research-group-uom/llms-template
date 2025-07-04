import boto3
import json

from botocore.exceptions import ClientError
from credentials import get_bedrock_client

def llama(first_paragraph, data):
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = get_bedrock_client()

    # Set the model ID, e.g., Llama 3 70b Instruct.
    model_id = "arn:aws:bedrock:us-east-1:043309345392:inference-profile/us.meta.llama3-3-70b-instruct-v1:0"
    i = 0
    all_responses = ''

    for person in data:
        i += 1
        print(f"{i}/{len(data)}")

        # Define the prompt for the model.
        prompt = f"""Please analyze the following PDF document content and provide a summary of its key points:
    
        <document_content>
        {person}
        </document_content>
    
        < Separate the piece of <Greek Text> extracted from a hiring decision exclusively into fields with the following <Format>, taking into account the <Descriptions> of the fields. Return the result exclusively using the provided <Format> for …….>
        <Format>:
        Person has_last_name <Last_Name> 
        Person has_first_name <First_Name> 
        Person has_father’s_name <Father’s_Name>  
        Government_agency has_name <Name> 
        Employment has_ from_date <From_Date>
        Employment has_ thru_date < Thru_Date>
        Employment has_"ID"_employee_number <"ID"_Employee_Number>
        Employment has_employment_type <Employment_Type>
        Position_Type has_title <Title>
        Position_Type has_branch <Branch>
        Position_Type has_specialization <Specialization>
        Position_Type is_designated_for_education_type <Education_Type>
        Position_Type has_grade <Grade>
        Position_Type has_pay_grade <Pay_Grade>
        Position_Type has_salary_step <Salary_Step>
        Position_Type has_standard_hours_per_week <Standard_Hours_Per_Week>
        Position_Type entails_employment_relationship <Employment_Relationship>
        Management_Area has_management_area_name <Management_Area_Name>
        Management_Area is_an_example_of_management_area_type <Management_Area_type>
        Regional_government_agency has_regional_agency_name <Regional_Agency_Name> 
         
        <Descriptions>:
        Last name: <The one and only one last name of a person>
        First name: <The one and only one first name of a person>
        Father’s name: <The one and only one father’s name of a person>
        Name: < The one and only one name of the government agency that issues the hiring decision>
        From date: <The one and only one date of publication of the hiring decision in the Government Gazette (ΦΕΚ)>
        Thru date: <The one and only one date that the employment ends. Take into account that the end of academic year (“διδακτικό έτος”) is “30/06/….”, where “….” represents the year, while the end of the school year (“σχολικό έτος”) is “31/08/….”. In the case of a two-year probationary appointment, this does not mean that his or her employment ends after two years>
        "ID" employee number: <The one and only one six-digit “ID” number of an employee. This number may not appear in some decisions.>
        Employment type: <The one and only one type of employment. Allowed values: “Διορισμός”, “Πρόσληψη”>
        Title: <The one and only one title of a position type. Allowed values: Εκπαιδευτικός πρωτοβάθμιας εκπαίδευσης, Εκπαιδευτικός δευτεροβάθμιας εκπαίδευσης, Εκπαιδευτικός πρωτοβάθμιας και δευτεροβάθμιας εκπαίδευσης, Ειδικό Εκπαιδευτικό Προσωπικό (ΕΕΠ), Ειδικό Βοηθητικό Προσωπικό (ΕΒΠ)>
        Branch: <The one and only one branch in which a position is classified>
        Specialization: < The one and only one specialization in which a position is classified>
        Education Type: <The one and only one education type for which a position is designated. Allowed values: Γενική Εκπαίδευση, Ειδική Αγωγή και Εκπαίδευση>
        Grade: <The one and only one grade in which a position is classified. The grades of teachers are “Γ”, “B”, “A”. “Γ” is the introductory grade. Allowed values: “Εισαγωγικός”, “Γ”, “B”, “A”>
        Pay Grade: < The one and only one education category in which a position is classified. Allowed values: “Πανεπιστημιακής Εκπαίδευσης (ΠΕ)”, “Τεχνολογικής Εκπαίδευσης (ΤΕ)”, “Δευτεροβάθμιας Εκπαίδευσης (ΔΕ)”>
        Salary step: <The one and only one salary step in which a position is classified. The salary steps of teachers are “ΜΚ1”, “ΜΚ2”, …, “ΜΚ19”. “ΜΚ1” is the introductory salary step. Allowed values: “Εισαγωγικό”, “ΜΚ1”, “ΜΚ2”, …, “ΜΚ19”>
        Standard hours per week: <The number of hours an employee is typically scheduled to work in a week, as defined by their employment agreement or job classification. Allowed values: “Πλήρους ωραρίου”, “Μειωμένου ωραρίου”. In some hiring decisions this information may not appear>
        Employment Relationship: <The one and only one employment relationship entailed by the position. Allowed values: Μόνιμος, Μόνιμος με διετή δοκιμαστική θητεία, Προσωρινός αναπληρωτής με σχέση εργασίας Ιδιωτικού Δικαίου Ορισμένου Χρόνου, Ωρομίσθιος>
        Management area name: <The one and only one name of a specific management area (e.g. “Α΄ ΑΝΑΤ. ΑΤΤΙΚΗΣ (Δ.Ε.)”)>
        Management area type: <The one and only one type of management area. Allowed values: Περιοχή Διορισμού, Περιοχή Τοποθέτησης, Περιοχή Πρόσληψης, Περιοχή Μετάταξης> 
        Regional_Agency_Name: <The one and only one name of the regional agency of the Ministry of Education (e.g., Δ.Ε. Α΄ ΑΘΗΝΑΣ), which has jusridiction over a geographic area>
        <Greek text>: 
        …"""

        # Embed the prompt in Llama 3's instruction format.
        formatted_prompt = f"""
        <|begin_of_text|><|start_header_id|>user<|end_header_id|>
        {first_paragraph + " " + prompt}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        # Format the request payload using the model's native structure.
        native_request = {
            "prompt": formatted_prompt,
            "max_gen_len": 4096,
            "temperature": 0.5,
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        try:
            # Invoke the model with the request.
            response = client.invoke_model(modelId=model_id, body=request)

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        response_text = model_response["generation"]

        all_responses +=  response_text + "\n\n\n"

    return all_responses


