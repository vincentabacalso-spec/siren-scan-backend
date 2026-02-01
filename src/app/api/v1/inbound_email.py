from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional
from typing import cast
from app.firebase import db
from app.services.llm_wrapper import LLM_interface
from app.services.virus_total import scan_url, scan_file
from app.services.html_parser import parse_html_content
from app.services.HIBP import HIBP_check
from app.services.model import model_interface
from app.services.email_hasher import hash_email
from google.cloud.firestore_v1 import DocumentSnapshot
import logging
import json
import tempfile


router = APIRouter()

@router.post("/mailgun/inbound")
async def inbound_email(request: Request, attachment: Optional[UploadFile] = None):
    try:
        form = await request.form()
        sender = form.get("sender")
        subject = form.get("subject")
        body_plain = form.get("body-plain")
        body_html = form.get("body-html")
        inbound_id = form.get("token")
        file = form.get("attachment-1") 

        
        print("---- Form Contents ----")
        for key, value in form.items():
            print(f"{key}: {type(value)} -> {value}")
        print("-----------------------")
        print(file)
        contents = await file.read()  # this is the full PDF as bytes
        print(contents[:200])  # print first 200 bytes to inspect
        await file.seek(0)  

        # if subject is None or body_plain is None or body_html is None:
        #     return JSONResponse(status_code=400, content={"error": "Missing required email fields."})
        # else:
        #     #check for attachment file. Only 1 file and pdf only
            
        #     #Determine if Phishing or Legitimate via model

        #     model_arg = f"Subject: {subject}\n\n{body_plain}"
        #     model_result = model_interface(model_arg)

        #     hashed_email = hash_email(str(sender).lower().strip())
        #     #processing email and saving to DB
        #     email_data = {
        #         "sender": hashed_email,
        #         "inbound_id": inbound_id,
        #         "subject": subject,
        #         "body_plain": body_plain,
        #         "body_html": body_html, 
        #         "model_result": model_result
        #     }

        #     doc_ref = db.collection("inbound_emails").document()
        #     doc_ref.set(email_data)
        #     email_data_id = doc_ref.id
            
        #     #processing HIBP and saving to DB
        #     hibp_id = f"hibp_{hashed_email}"
        #     doc_ref = db.collection("hibp_analyses").document(hibp_id)
        #     doc_snapshot = cast(DocumentSnapshot, doc_ref.get())

        #     if doc_snapshot.exists:
        #         logging.info(f"Record for {hashed_email} already exists, skipping write.") 
        #     else:
        #         HIBP_response = HIBP_check(sender)
        #         if HIBP_response:
        #             hibp_analysis = {
        #                 "email": hashed_email,
        #                 "breaches": [
        #                     {
        #                         "Name": b["Name"], 
        #                         "Title": b.get("Title", ""),
        #                         "Description": b.get("Description", ""),
        #                         "DataClasses": b.get("DataClasses", []),
        #                         "BreachDate": b.get("BreachDate", ""),
        #                     } for b in HIBP_response
        #                 ] 
        #             }

        #             db.collection("hibp_analyses").document(hibp_id).set(hibp_analysis)
                
        #     # processing virus total url and saving to DB
        #     isURL = parse_html_content(body_html)
        #     if isURL:
        #         url_response = scan_url(isURL)
        #         url_id = url_response.get("meta",{}).get("url_info", {}).get("id", "")
        #         url_db_id = f"url_{url_id}"
        #         doc_ref = db.collection("url_analyses").document(url_db_id)
        #         doc_snapshot = cast(DocumentSnapshot, doc_ref.get())

        #         if doc_snapshot.exists:
        #             logging.info(f"Record for URL ID {url_id} already exists, skipping write.") 
        #         else: 
        #             url_analysis = {
        #                 "analysis_id": url_response.get("meta",{}).get("url_info", {}).get("id", ""),
        #                 "url": url_response.get("meta", {}).get("url_info", {}).get("url", ""),
        #                 "stats": url_response.get("data", {}).get("attributes", {}).get("stats", {}), 
        #                 "results": url_response.get("data", {}).get("attributes", {}).get("results", {}),
        #                 "inbound_email_id": inbound_id, 
        #                 "email_sender": hashed_email
        #             }
                    
        #             db.collection("url_analyses").document(url_id).set(url_analysis)
        #     else: 
        #         logging.info("No URL found in the email body.")
            
            
        #     #llm synthesis report
        #     LLM_res = LLM_interface(model_result, json.dumps(url_analysis), body_plain) #take note of attachments
        #     db.collection("inbound_emails").document(email_data_id).update({"LLM_synthesis": LLM_res})

        #     return JSONResponse(status_code=200, content={"message": "Inbound email processed successfully."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})