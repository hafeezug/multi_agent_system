from transformers import pipeline

class LLMClient:
    def __init__(self, model="distilbert-base-uncased-finetuned-sst-2-english"):
        # Loading HuggingFace model for text classification
        self.classifier = pipeline("text-classification", model=model)

    def classify_complexity(self, query):
        # using model to classify query
        result = self.classifier(query)[0]
        label = "simple"
        conf = float(result["score"])
        text = query.lower()

        # Custom rules for overriding model output (heuristics)
        if any(w in text for w in ["compare", "analyze", "trade-off", "efficiency", "methodology", "papers"]):
            label = "complex"
        elif len(text.split()) > 6:
            label = "medium"
        return label, conf
