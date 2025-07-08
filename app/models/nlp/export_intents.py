# app/nlp/export_intents.py

import csv
from app import db, create_app
from app.models.nlp.Nlp_Intents import NlpIntent

def export_intents_to_csv():
    intents = NlpIntent.query.all()
    with open('intents_export.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['IntentID', 'Name', 'Description', 'Examples', 'Response'])
        for intent in intents:
            writer.writerow([
                intent.IntentID,
                intent.Name,
                intent.Description,
                intent.Examples,
                intent.Response
            ])
    print("✅ Intentها با موفقیت در فایل intents_export.csv ذخیره شدند.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        export_intents_to_csv()
