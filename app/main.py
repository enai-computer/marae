from fastapi import FastAPI
from uuid import UUID

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.put("/spaces/{user_id}/webContent/{web_content_id}")
def update_web_content(user_id: UUID, web_content_id: UUID, web_content: dict):
    return {"status": "ok"}

@app.put("/spaces/{user_id}/note/{note_id}")
def update_note(user_id: UUID, note_id: UUID, note: dict):
    return {"status": "ok"}

@app.put("/spaces/{user_id}/pdf/{pdf_id}")
def update_pdf(user_id: UUID, pdf_id: UUID, pdf: dict):
    return {"status": "ok"}

# Delete
@app.delete("/spaces/{user_id}/webContent/{web_content_id}")
def delete_web_content(user_id: UUID, web_content_id: UUID):
    return {"status": "ok"}

@app.delete("/spaces/{user_id}/note/{note_id}")
def delete_note(user_id: UUID, note_id: UUID):
    return {"status": "ok"}

@app.delete("/spaces/{user_id}/pdf/{pdf_id}")
def delete_pdf(user_id: UUID, pdf_id: UUID):
    return {"status": "ok"}

