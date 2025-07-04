import json
from botocore.exceptions import ClientError
from credentials import get_bedrock_client

def claude3_7(first_paragraph, data):
    # Create an Amazon Bedrock Runtime client.
    brt = get_bedrock_client()

    # Set the model ID
    model_id = "arn:aws:bedrock:us-east-1:043309345392:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"

    all_responses = ""
    i = 0
    for person in data:
        i += 1
        print(f"{i}/{len(data)}")
        # Define the prompt for the model
        prompt = f"""Please analyze the following PDF document content and provide a summary of its key points:
    
        <document_content>
        {person}
        </document_content>
    
        < Separate the piece of <Greek Text> extracted from a position assignment decision exclusively into fields with the following <Format>, taking into account the <Descriptions> of the fields. Return the result exclusively using the provided <Format> for ….>
        <Format>:
        Person has_last_name <Last_Name> 
        Person has_first_name <First_Name> 
        Person has_father’s_name <Father’s_Name> 
        Employment has_ "ID"_employee_number <"ID"_Employee_Number>
        Position_assignment_<N> has_from_date <From_Date>
        Position_assignment_<N> has_thru_date <Thru_Date>
        Position_assignment_<N> has_position_assignment_type <Position_Assignment_Type> 
        Position_<M> has_kind_of_position <Kind_Of_Position>
        Position_<M> has_status <Status>
        Position_<M> has_working_hours_per_week <Working_Hours_Per_Week>
        Position_Type has_title <Title>
        Position_Type has_branch <Branch>
        Position_Type has_specialization <Specialization>
        Position_Type is_designated_for_education_type <Education_Type>
        Position_Type has_standard_hours_per_week <Standard_Hours_Per_Week>
        Position_Type entails_employment_relationship <Employment_Relationship> 
        Government_agency_<Z> has_name <Name> 
        
        Where <N> the number of Position Assignment.
        Where <M> the number of Position.
        Where <Z> the number of Government Agency.
         
        <Descriptions>:
        Last name: <The one and only one last name of a person>
        First name: <The one and only one first name of a person>
        Father’s name: <The one and only one father’s name of a person>
        "ID" employee number: <The one and only one six-digit “ID” number of an employee. This number may not appear in some decisions.>
        From date: <The one and only one date that the position assignment starts.>
        Thru date: < The one and only one date that the position assignment ends. Take into account that the end of academic year (“διδακτικό έτος”) is “30/06/….”, where “….” represents the year, while the end of the school year (“σχολικό έτος”) is “31/08/….”.>
        Position assignment type: <The one and only one type of position assignment. Allowed values: «Τοποθέτηση», “Μετάθεση εντός ΠΥΣΔΕ”, “Οριστική Τοποθέτηση, “Διάθεση”, “Μετάταξη”>
        Kind of position: < The one and only one kind of position, depending on whether it is permanent or temporary. Allowed values: Οργανική, Λειτουργική ανάγκη, Διδακτική ανάγκη>
        Status: <The one and only one status of a position depending on whether it is vacant or filled. Allowed values: Κενή, Καλυμμένη>
        Working hours per week: <The number of hours a teacher works per week>
        Title: <The one and only one title of a position type. Allowed values: Εκπαιδευτικός πρωτοβάθμιας εκπαίδευσης, Εκπαιδευτικός δευτεροβάθμιας εκπαίδευσης, Εκπαιδευτικός πρωτοβάθμιας και δευτεροβάθμιας εκπαίδευσης, Ειδικό Εκπαιδευτικό Προσωπικό (ΕΕΠ), Ειδικό Βοηθητικό Προσωπικό (ΕΒΠ)>
        Branch: <The one and only one branch in which a position is classified>
        Specialization: < The one and only one specialization in which a position is classified>
        Education Type: <The one and only one education type for which a position is designated. Allowed values: Γενική Εκπαίδευση, Ειδική Αγωγή και Εκπαίδευση>
        Standard hours per week: <The number of hours an employee is typically scheduled to work in a week, as defined by their employment agreement or job classification. Allowed values: “Πλήρους ωραρίου”, “Μειωμένου ωραρίου”>
        Employment Relationship: <The one and only one employment relationship entailed by the position. Allowed values: Μόνιμος, Μόνιμος με διετή δοκιμαστική θητεία, Προσωρινός αναπληρωτής με σχέση εργασίας Ιδιωτικού Δικαίου Ορισμένου Χρόνου, Ωρομίσθιος>
        Name: < The one and only one name of the government agency, that defines the position (e.g., “ΕΠΑΛ ΝΙΚΗΤΗΣ”)> 
        <Greek text>: 
        …"""

        final_prompt = first_paragraph+" "+prompt
        # Format the request payload (back to simple text)
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 131072,
            "top_k": 250,
            "stop_sequences": [],
            "temperature": 0.7,
            "top_p": 0.999,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": final_prompt
                        }
                    ]
                }
            ]
        }

        # Convert the native request to JSON
        request = json.dumps(native_request)

        try:
            # Invoke the model with the request
            response = brt.invoke_model(modelId=model_id, body=request)

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)

        # Decode the response body
        model_response = json.loads(response["body"].read())

        # Extract and print the response text
        response_text = model_response['content'][0]['text']

        all_responses += response_text + "\n\n\n"

    return all_responses