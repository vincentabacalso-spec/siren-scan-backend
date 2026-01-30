from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional
from firebase_admin import storage
from app.firebase import db
from app.services.llm_wrapper import LLM_interface
from app.services.virus_total import scan_url, scan_file
from app.services.html_parser import parse_html_content

router = APIRouter()

@router.post("/mailgun/inbound")
async def inbound_email(request: Request, attachment: Optional[UploadFile] = None):
    try:
        form = await request.form()

        # if attachment:
        #     file_content = await attachment.read()
        #     filename = attachment.filename

        sender = form.get("sender")
        recipient = form.get("recipient")
        subject = form.get("subject")
        body_plain = form.get("body-plain")
        body_html = form.get("body-html")
        file = form.get("attachment-1")  # Example for first attachment
    
        print(f"Received email from {sender} to {recipient} with subject '{subject}'")
        print(f"Body (plain): {body_plain}")
        print(f"Body (HTML): {body_html}")
        print(f"Attachment: {file if file else 'No attachment'}")


        # email_data = {
        #     "sender": sender,
        #     "recipient": recipient,
        #     "subject": subject,
        #     "body_plain": body_plain,
        #     "body_html": body_html
        # }

        # db.collection("inbound_emails").document().set(email_data)



        # isBodyHTML = parse_html_content(body_html)
        # if isBodyHTML:
        #     url_response = scan_url(isBodyHTML)
        #     url_analysis = {
        #         "analysis_id": url_response.get("meta",{}).get("url_info", {}).get("id", ""),
        #         "url": url_response.get("meta", {}).get("url_info", {}).get("url", ""),
        #         "stats": url_response.get("data", {}).get("attributes", {}).get("stats", {}), 
        #         "results": url_response.get("data", {}).get("attributes", {}).get("results", {})
        #     }
        #     url_id = url_response.get("meta",{}).get("url_info", {}).get("id", "")
        #     db.collection("url_analyses").document(url_id).set(url_analysis)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

     
    
    

    #re write the attachment logic 
    # Return parsed data as JSON

'''
call the services here then store the results in firebase
- check if there are attachments so you can call the functions appropriately


'''