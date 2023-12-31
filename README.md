# FitBit Support Chatbot
  
This project was part of the Maker Suite Sprint and creates a OCR processor to transcript FitBit User Manual PDF into a text file then uses Google Cloud Generative AI + Dialogflow to create a chatbot that answers questions about the FitBit User Manual.  
  
Guidelines:  
<b>  Clone the repo</b>  
<b>  Create a bucket</b>  
<b>  Create a processor in Document AI and run DocumentAI.py</b>  
<b>  Test prediction.py locally (Cloud Run folder)</b>  
<b>  Run</b> gcloud builds submit --tag gcr.io/your project_id/container_name . --timeout=85000  
<b>  Run</b> gcloud run deploy container_name --image gcr.io/your_project_id/container_name --min-instances 1 --allow-unauthenticated --memory 512Mi --max-instances 1 --region us-central1  
<b>  Set up Dialogflow</b>   
<b>  Run</b> Dialogflow_add_names_entity_csv.py to populate entity names. Set up flows and choose Dialogflow Messenger in Integrations  
<b>  Use</b> chatbot_html_embed.html to add Dialogflow Messenger to your website  
<img src = "https://github.com/RubensZimbres/fitbit-public/blob/main/gdee.png">  

<b> MakerSuite </b>
<img src = "https://github.com/RubensZimbres/fitbit-public/blob/main/makersuite.png">  

<b> Architecture </b>
<img src = "https://github.com/RubensZimbres/fitbit-public/blob/main/fitbit-2023-08-25-1851.png">  
