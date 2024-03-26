from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import re
import requests
import json
import csv

openai_api_key = "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"
model = ChatOpenAI(api_key=openai_api_key, temperature=0)


class ReceiptInfo(BaseModel):
    total_amount: float = Field(description="Total amount paid on the receipt")
    date: str = Field(description="Date on the receipt")
    category: str = Field(description="Company tax category")


parser = PydanticOutputParser(pydantic_object=ReceiptInfo)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

ocr_results_file = 'ocr_results.csv'
with open(ocr_results_file, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        receipt_text = row[0]
    company_query = f"{receipt_text}\n Extract the total amount paid after everything and date from the receipt text provided below. Also from the company name and products purchased, extract the tax category it belongs to: Groceries, Clothes, Office, Vehicle, Meals, Rent, Phone & Utilities, Supplies, or Assets"
    result = chain.invoke(
        {"query": company_query, "openai_api_key": openai_api_key})

    # Print the extracted information
    print("Total Amount Paid:", result.total_amount)
    print("Date:", result.date)
    print("Category:", result.category)
# import csv
# from langchain.output_parsers import PydanticOutputParser
# from langchain.prompts import PromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_openai import ChatOpenAI
# import openpyxl

# openai_api_key = "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"
# model = ChatOpenAI(api_key=openai_api_key, temperature=0)


# class ReceiptInfo(BaseModel):
#     total_amount: float = Field(description="Total amount paid on the receipt")
#     date: str = Field(description="Date on the receipt")
#     category: str = Field(description="Company tax category")


# parser = PydanticOutputParser(pydantic_object=ReceiptInfo)

# prompt = PromptTemplate(
#     template="Answer the user query.\n{format_instructions}\n{query}\n",
#     input_variables=["query"],
#     partial_variables={
#         "format_instructions": parser.get_format_instructions()}
# )

# chain = prompt | model | parser

# ocr_results_file = 'ocr_results.csv'
# output_file = 'receipt_info.xlsx'

# try:
#     workbook = openpyxl.load_workbook(output_file)
# except FileNotFoundError:
#     workbook = openpyxl.Workbook()

# category_worksheets = {}

# with open(ocr_results_file, 'r', newline='') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         receipt_text = row[0]

#         company_query = f"Extract the total final amount paid after everything and date from the receipt text provided below. Also from the company name and products purchased, extract the tax category it belongs to: Groceries, Clothes, Office, Vehicle, Meals, Rent, Phone & Utilities, Supplies, or Assets\n{receipt_text}"

#         result = chain.invoke(
#             {"query": company_query, "openai_api_key": openai_api_key})

#         if isinstance(result, ReceiptInfo):
#             category = result.category.strip()

#             if category not in category_worksheets:
#                 if category in workbook.sheetnames:
#                     category_worksheets[category] = workbook[category]
#                 else:
#                     category_worksheets[category] = workbook.create_sheet(
#                         title=category)
#                     category_worksheets[category].append(
#                         ["Date", "Total Amount Paid"])

#             category_worksheets[category].append(
#                 [result.date, result.total_amount])
#         else:
#             print("Failed to extract information from the receipt.")

# if 'Sheet' in workbook.sheetnames:
#     workbook.remove(workbook['Sheet'])

# workbook.save(output_file)

# openai_api_key = "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"
# openai_api_url = "https://api.openai.com/v1/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {openai_api_key}"
# }
# # Initialize the ChatOpenAI model

# # Define the ReceiptInfo Pydantic model


# class ReceiptInfo(BaseModel):
#     company_name: str = Field(description="Name of the company on the receipt")
#     total_amount: float = Field(description="Total amount paid on the receipt")
#     date: str = Field(description="Date on the receipt")


# # Define the prompt template
# def extract_info_from_receipt(receipt: str) -> ReceiptInfo:
#     prompt_template = f"Extract the company name, total amount paid, and date from the receipt text provided below:\n{receipt}"
#     user_content = 'Answer the user query.\nThe output should be formatted as a JSON instance that conforms to the JSON schema. {prompt_template}'
#     user_content = user_content.replace('{prompt_template}', prompt_template)

#     data = {
#         "temperature": 0,
#         "model": "gpt-3.5-turbo",
#         'messages': [
#             {"role": "user", "content": user_content}
#         ],
#         "n": 1
#     }

#     response = requests.post(openai_api_url, json=data, headers=headers)
#     result = response.json()
#     result_content = result["choices"][0]["message"]["content"]
#     result_content = json.loads(result_content)
#     # Define the PromptTemplate with receipt text

#     # Return the parsed ReceiptInfo object
#     return result_content


# # Example receipt text
# ocr_results_file = 'ocr_results.csv'
# with open(ocr_results_file, 'r', newline='') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         receipt_text = row[0]
# # Extract information from the receipt text
#     receipt_info = extract_info_from_receipt(receipt_text)

#     print(receipt_info)
#     # Print the extracted information
#     print("Company Name:", receipt_info['companyName'])
#     print("Total Amount Paid:", receipt_info['totalAmountPaid'])
#     print("Date:", receipt_info['date'])
