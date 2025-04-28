# Attempt to build a LLM for determining relevancy for specific stock articles. 
# Currently running from curated data (~200 entries) of labeled articles
# Each Articles are listed as yes or no for relevancy


# X/Y plot -> Sentiment Reasoning (X)  Relevent (Y)
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments


print(TrainingArguments)




df = pd.read_csv(r'C:\Users\Amritpal Rajput\Desktop\Personal Projects\LLM\AAPL_news_sentiment_final_labeled.csv')

texts = df['Title'].tolist()
labels = df['Relevant'].tolist()

labels = [1 if str(label).lower() == "yes" or str(label) == "1" else 0 for label in labels]

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

tokenizer = BertTokenizerFast.from_pretrained('yiyanghkust/finbert-tone')

train_encoding = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encoding = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encoding, labels):
        self.encoding = encoding
        self.labels = labels
    
    def __getitem__(self,idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encoding.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)


train_dataset = NewsDataset(train_encoding, train_labels)
val_dataset = NewsDataset(val_encoding, val_labels)


#model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=2)

model = BertForSequenceClassification.from_pretrained(
    'yiyanghkust/finbert-tone',
    num_labels=2,
    ignore_mismatched_sizes=True
)



training_args= TrainingArguments(
    output_dir='./finbert-results',
    num_train_epochs=10,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)


import numpy as np

def compute_metrics(eval_pred):
    logits,labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = (predictions == labels).mean()
    return {"accuracy": acc}


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()


model.save_pretrained("./finbert_relevance_model")
tokenizer.save_pretrained("./finbert_relevance_model")
