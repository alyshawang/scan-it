from pathlib import Path
from transformers import LayoutLMTokenizerFast, LayoutLMForTokenClassification, TrainingArguments, Trainer
import os

import torch
from PIL import Image
# Define paths and configurations
dataset_directory = Path('/Users/alyshawang/Documents/ReceiptScanner/data')
labels_file = Path(
    '/Users/alyshawang/Documents/ReceiptScanner/data/labels.txt')

# Initialize LayoutLM model and tokenizer
model = LayoutLMForTokenClassification.from_pretrained(
    "microsoft/layoutlm-base-uncased")
tokenizer = LayoutLMTokenizerFast.from_pretrained(
    "microsoft/layoutlm-base-uncased")


# Read training data
with open(dataset_directory / "train.txt", "r") as f:
    train_data = f.read().splitlines()

# Read bounding box information
with open(dataset_directory / "train_box.txt", "r") as f:
    train_boxes = [line.split() for line in f.read().splitlines()]

# Read image data
train_images = []
with open(dataset_directory / "train_image.txt", "r") as f:
    for line in f:
        image_path = line.strip().split()[-1]
        image = Image.open(image_path).convert("RGB")
        train_images.append(image)

# Read labels
with open(dataset_directory / "labels.txt", "r") as f:
    label_list = f.read().splitlines()

# Tokenize training data
tokenized_inputs = tokenizer(
    train_data, padding=True, truncation=True, return_tensors="pt")

# Create attention masks
attention_masks = []
for input_ids in tokenized_inputs["input_ids"]:
    attention_mask = [1] * len(input_ids)
    attention_masks.append(attention_mask)
attention_masks = torch.tensor(attention_masks)

# Convert bounding box coordinates to tensor
bbox = []
for box in train_boxes:
    coords = [int(coord) for coord in box.split()]
    bbox.append(coords)
bbox = torch.tensor(bbox)

# Convert image data to tensors
image_tensors = [tokenizer.convert_image_to_tensors(
    image)["pixel_values"] for image in train_images]

# Combine input data
train_dataset = {
    "input_ids": tokenized_inputs["input_ids"],
    "bbox": bbox,
    "attention_mask": attention_masks,
    "image": image_tensors,
    "labels": torch.tensor(label_list)  # Convert labels to tensor
}

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

# Create Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

# Train the model
trainer.train()
