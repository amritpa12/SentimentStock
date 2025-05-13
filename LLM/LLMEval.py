from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import numpy as np

model = BertForSequenceClassification.from_pretrained(
    r"C:\Users\Amritpal Rajput\Desktop\Personal Projects\LLM\finbert-results\checkpoint-200",
    local_files_only=True
    )

# tokenizer = BertTokenizerFast.from_pretrained(
#     r"C:\Users\Amritpal Rajput\Desktop\Personal Projects\LLM\finbert-results\checkpoint-200",
#     local_files_only=True
#     )


tokenizer = BertTokenizerFast.from_pretrained("yiyanghkust/finbert-pretrain")  # or the tokenizer you trained with



def classify_article(text):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)


    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).numpy()[0]
    prediction = np.argmax(probabilities)

    label = "Relevant" if prediction == 1 else "Not Relevant"
    confidence = probabilities[prediction]

    return {
        "label": label,
        "confidence": float(confidence),
        "probabilities": {"Not Relevant": float(probabilities[0]), "Relevant": float(probabilities[1])}
    }

# Example usage
article_text = """
Apple Inc. reported record-breaking sales of its new iPhone models this quarter,
which analysts say is a strong indicator of consumer confidence and economic recovery.
Shares of the tech giant rose by 5% in after-hours trading following the announcement.
Investors are optimistic that the momentum will continue into the next quarter.
"""
result = classify_article(article_text)
print(result)