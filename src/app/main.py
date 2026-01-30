from fastapi import FastAPI
from app.api.v1.inbound_email import router as mail_router
from app.firebase import db

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.post("/test-write")
# async def create_test_document():
#     try:
#         doc_ref = db.collection("test_collection").document("first_doc")
        
#         # .set() actually returns a result object
#         result = doc_ref.set({
#             "message": "Hello from FastAPI!",
#             "timestamp": "2026-01-24",
#             "status": "Success"
#         })
        
#         # This will print the exact time Google recorded the save in your terminal
#         print(f"🔥 Firebase updated at: {result.update_time}")
        
#         return {
#             "status": "Document created successfully!",
#             "update_time": str(result.update_time) 
#         }
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         return {"error": str(e)}

app.include_router(mail_router, prefix="/api/v1")

