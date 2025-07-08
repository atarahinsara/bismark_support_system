# app/nlp/ner_model_loader.py

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

_ner_pipeline_instance = None

def get_ner_pipeline():
    global _ner_pipeline_instance
    if _ner_pipeline_instance is None:
        print("🔄 بارگذاری مدل BERT برای NER...")
        model_name = "HooshvareLab/bert-base-parsbert-ner-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        _ner_pipeline_instance = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
        print("✅ مدل BERT بارگذاری شد.")
    return _ner_pipeline_instance
