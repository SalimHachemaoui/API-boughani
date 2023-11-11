import shutil
import os
import schedule
import time

def delete_pdf_folder():
    folder_path = 'PDFupload'
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print("Dossier PDFupload supprimé.")
    else:
        print("Dossier PDFupload introuvable.")

# Planifier la suppression toutes les 24 heures
schedule.every(24).hours.do(delete_pdf_folder)

# Boucle pour exécuter les tâches planifiées
while True:
    schedule.run_pending()
    time.sleep(1)
