# import cv2
# from paddleocr import PaddleOCR
# import csv

# ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)

# camera = cv2.VideoCapture(0)

# if not camera.isOpened():
#     print("Error: Unable to access the camera.")
#     exit()

# while True:
#     ret, frame = camera.read()

#     cv2.imshow('Camera', frame)

#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#     elif key == ord('s'):
#         cv2.imwrite('temp_image.jpg', frame)

#         result = ocr.ocr('temp_image.jpg', cls=True)

#         extracted_text = ' '.join([word[1][0]
#                                   for line in result for word in line])

#         print("Extracted Text:")
#         print(extracted_text)

#         with open('ocr_results.csv', 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([extracted_text])

# camera.release()
# cv2.destroyAllWindows()
import cv2
import firebase_admin
from firebase_admin import credentials, storage
from paddleocr import PaddleOCR
import csv
import sys

# Initialize Firebase Admin SDK
cred = credentials.Certificate(
    "/Users/alyshawang/Documents/ReceiptScanner/receiptscanner-7df72-firebase-adminsdk-68x0t-3ec3d2e781.json")
firebase_admin.initialize_app(
    cred, {"storageBucket": "receiptscanner-7df72.appspot.com"})

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)
bucket = storage.bucket()

# Function to process an image


def process_image(image_bytes):
    with open('temp_image.jpg', 'wb') as file:
        file.write(image_bytes)
    frame = cv2.imread('temp_image.jpg')
    result = ocr.ocr(frame, cls=True)
    extracted_text = ' '.join([word[1][0] for line in result for word in line])
    return extracted_text


# Iterate through all files in the Firebase Storage bucket
folder_name = sys.argv[1]

# Iterate through all files in the Firebase Storage folder
blobs = bucket.list_blobs(prefix=folder_name + '/')
for blob in blobs:
    # Download image from Firebase Storage
    image_bytes = blob.download_as_bytes()

    # Process the image
    extracted_text = process_image(image_bytes)

    # Print or save the extracted text
    print("Extracted Text:")
    print(extracted_text)

    # Optionally, save the extracted text to a CSV file
    with open('ocr_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([extracted_text])
    blob.delete()

# Close any open windows
cv2.destroyAllWindows()


# import cv2
# from paddleocr import PaddleOCR
# import re

# # Initialize PaddleOCR
# ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)

# # Function to extract relevant information from the extracted text


# def extract_information(extracted_text):
#     company_name = ""
#     date = ""
#     total_amount = ""

#     # Extract company name
#     company_name_match = re.search(r'^([^,]+)', extracted_text)
#     if company_name_match:
#         company_name = company_name_match.group(1).strip()

#     # Extract date
#     date_match = re.search(
#         r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{1,2},\d{4}', extracted_text)
#     if date_match:
#         date = date_match.group().strip()

#     # Extract total amount
#     total_match = re.search(r'TOTAL:\s*\$\s*([0-9.]+)', extracted_text)
#     if total_match:
#         total_amount = total_match.group(1).strip()

#     return company_name, date, total_amount


# # Initialize the camera
# camera = cv2.VideoCapture(0)

# # Check if the camera is opened successfully
# if not camera.isOpened():
#     print("Error: Unable to access the camera.")
#     exit()

# while True:
#     # Capture frame-by-frame
#     ret, frame = camera.read()

#     # Display the captured frame
#     cv2.imshow('Camera', frame)

#     # Wait for 'q' key to quit and 's' key to capture and process the image
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#     elif key == ord('s'):
#         # Save the captured frame to a temporary file
#         cv2.imwrite('temp_image.jpg', frame)

#         # Perform OCR on the captured image
#         result = ocr.ocr('temp_image.jpg', cls=True)

#         # Concatenate all lines of text into a single string
#         extracted_text = ' '.join([word[1][0]
#                                   for line in result for word in line])

#         # Extract relevant information from the extracted text
#         company_name, date, total_amount = extract_information(extracted_text)

#         # Print the extracted information
#         print("Company Name:", company_name)
#         print("Date:", date)
#         print("Total Amount:", total_amount)

# # Release the camera and close all OpenCV windows
# camera.release()
# cv2.destroyAllWindows()
