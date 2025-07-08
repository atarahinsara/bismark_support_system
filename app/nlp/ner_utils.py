# app/nlp/ner_utils.py

from app.nlp.ner_model_loader import get_ner_pipeline

def extract_names_fa(text):
    ner_pipeline = get_ner_pipeline()
    results = ner_pipeline(text)

    print("NER model output:", results)

    names = []
    current_name = []

    for entity in results:
        if entity['entity_group'].lower() in ['per', 'person']:
            current_name.append(entity['word'])
        else:
            if current_name:
                names.append(" ".join(current_name))
                current_name = []

    if current_name:
        names.append(" ".join(current_name))

    print("extract_names_fa output:", names)
    return names
