from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import threading
import schedule
import time
import shutil

from Algorithme.scraper import scrape_website, generate_summary
from Algorithme.summarizer import extract_text_from_pdf, generate_summary

# Initialize the FastAPI app
app = FastAPI()
@app.post("/scrape_and_summarize/")
async def scrape_and_summarize(url: str):
    content = scrape_website(url)
    if content:
        summary = generate_summary(content)
        return {"summary": summary}
    else:
        raise HTTPException(status_code=400, detail="Content could not be retrieved or summarized.")

@app.post("/summarize_pdf/")
async def summarize_pdf(pdf_file: UploadFile = File(...)):
    # Créer le dossier s'il n'existe pas
    os.makedirs("PDFupload", exist_ok=True)

    # Chemin où le fichier sera enregistré
    file_location = f"PDFupload/{pdf_file.filename}"

    # Enregistrer le fichier PDF
    with open(file_location, "wb") as file_object:
        file_object.write(await pdf_file.read())

    # Extraire le texte du PDF
    content = extract_text_from_pdf(file_location)
    if content:
        summary = generate_summary(content)
        return {"text": content, "summary": summary}
    else:
        raise HTTPException(status_code=400, detail="Content could not be extracted or summarized.")


def delete_pdf_files():
    folder_path = 'PDFupload'
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                try:
                    os.remove(file_path)
                    print(f"Supprimé: {file_path}")
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file_path}: {e}")
    else:
        print("Dossier PDFupload introuvable.")


def run_schedule():
    print("salim")
    schedule.every(30).seconds.do(delete_pdf_files)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == "__main__":
    # Créer et démarrer le thread de planification
    schedule_thread = threading.Thread(target=run_schedule, daemon=True)
    schedule_thread.start()
    

    # Démarrer FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000)
