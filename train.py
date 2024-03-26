# import os
# from PIL import Image
# import torch
# from transformers import LayoutLMForTokenClassification, LayoutLMTokenizerFast
# from transformers import TrainingArguments, Trainer

# # Load necessary libraries

# # Load LayoutLM model and tokenizer
# model = LayoutLMForTokenClassification.from_pretrained(
#     "microsoft/layoutlm-base-uncased")
# tokenizer = LayoutLMTokenizerFast.from_pretrained(
#     "microsoft/layoutlm-base-uncased")

# # Set up training arguments
# training_args = TrainingArguments(
#     output_dir="./results",
#     num_train_epochs=3,
#     per_device_train_batch_size=8,
#     per_device_eval_batch_size=16,
#     warmup_steps=500,
#     weight_decay=0.01,
#     logging_dir="./logs",
# )

# # Define a function to load images and convert them to features


# def load_images_from_folder(folder_path, tokenizer, max_length):
#     images = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".jpg"):
#             img_path = os.path.join(folder_path, filename)
#             image = Image.open(img_path).convert("RGB")
#             encoding = tokenizer(
#                 image, return_tensors="pt", padding="max_length", max_length=max_length, truncation=True)
#             images.append(encoding)
#     return images


# # Define your dataset folder path and load images from it
# dataset_folder_path = "/Users/alyshawang/Downloads/task1&2_test(361p)"
# max_length = 512  # Adjust as needed
# train_images = load_images_from_folder(
#     dataset_folder_path, tokenizer, max_length)
# eval_images = load_images_from_folder(os.path.join(
#     dataset_folder_path, "eval"), tokenizer, max_length)

# # Create a custom dataset class


# class CustomDataset(torch.utils.data.Dataset):
#     def __init__(self, encodings):
#         self.encodings = encodings

#     def __getitem__(self, idx):
#         return self.encodings[idx]

#     def __len__(self):
#         return len(self.encodings)


# # Create train and eval datasets
# train_dataset = CustomDataset(train_images)
# eval_dataset = CustomDataset(eval_images)

# # Create Trainer object
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=eval_dataset,
# )

# # Train the model
# trainer.train()


import os
import pytesseract
from PIL import Image
import torch
from transformers import LayoutLMForTokenClassification, LayoutLMTokenizerFast, TrainingArguments, Trainer
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Initialize LayoutLM model and tokenizer
model = LayoutLMForTokenClassification.from_pretrained(
    "microsoft/layoutlm-base-uncased")
tokenizer = LayoutLMTokenizerFast.from_pretrained(
    "microsoft/layoutlm-base-uncased")

# Define the dataset folder path
dataset_folder_path = "/Users/alyshawang/Documents/ReceiptScanner/data"

# Function to preprocess images and extract text


# def preprocess_images(image_folder_path):
#     text_list = []
#     for filename in os.listdir(image_folder_path):
#         if filename.endswith(".jpg"):
#             image_path = os.path.join(image_folder_path, filename)
#             image = Image.open(image_path).convert("RGB")
#             # Perform OCR to extract text from the image
#             text = pytesseract.image_to_string(image)
#             print(text)
#             text_list.append(text)
#     return text_list


# # Preprocess images and extract text
# text_list = preprocess_images(dataset_folder_path)

# Tokenize the extracted text
tokenized_inputs = tokenizer(
    dataset_folder_path, padding=True, truncation=True, return_tensors="pt")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Define Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_inputs
)

# Train the model
trainer.train()

# Evaluate the model if you have an evaluation dataset
# trainer.evaluate(eval_dataset=eval_dataset)
