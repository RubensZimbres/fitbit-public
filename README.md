# FitBit Support Chatbot

Guidelines:  
<b></b>  Clone the repo
<b></b>  Create a bucket
<b></b>  Create a processor in Document AI and run DocumentAI.py
<b></b>  Test prediction.py locally (Cloud Run folder)
<b></b>  Run gcloud builds submit --tag gcr.io/your project_id/container_name . --timeout=85000  
<b></b>  Run gcloud run deploy container_name --image gcr.io/your_project_id/container_name --min-instances 1 --allow-unauthenticated --memory 4Gi --max-instances 8 --region us-central1  
<b></b>  Set up Dialogflow  
<b></b>  Run Dialogflow_add_names_entity_csv.py to populate entity names. Set up flows and choose Dialogflow Messenger in Integrations  
<b></b>  Use chatbot_html_embed.html to add Dialogflow Messenger to your website
