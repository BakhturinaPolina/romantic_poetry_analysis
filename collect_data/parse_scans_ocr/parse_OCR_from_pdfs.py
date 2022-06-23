""" Working with non-modern literature could be a very tricky task. Although there are several standardised data
sets created upon Gutenberg Project, if you decided to analyse something rare, such as our romantic poetry,
there will be no other way than to work with scanned books rather than with a nice txt.files. More than half of the
books included in this data set are simply scanned. It is impossible to simply "read" from such pages, using tools
like PyPDF2 library. But it's still possible to read contend of PDF files using OCR (Optical Character Recognition)!"""
import json
import os
import tempfile
from pathlib import Path
import pytesseract
from PIL import Image
from PIL import ImageFile
from pdf2image import convert_from_path

Image.MAX_IMAGE_PIXELS = None  # this setting will help us to disable 'DecompressionBombError'
ImageFile.LOAD_TRUNCATED_IMAGES = True  # this setting will help us to disable 'OSError: image file is truncated'

root = os.getcwd()

os.makedirs(f"{root}/ocr_output/jpeg", exist_ok=True) # dir to be used to store images created from pdf pages in the process

lines_of_text = []


def extract_text_from_pdf(rootdir):
          for i, path in enumerate(Path(rootdir).iterdir()):  # iterate though all subdirs in rootdir
                    if path.is_dir():
                              extract_text_from_pdf(path)  # call this function on the subdir
                    if path.is_file() and Path(path).suffix == '.pdf':
                              book_name = Path(path).stem
                              print(f"Processing book {i + 1}/{len(os.listdir(rootdir))}")
                              # Iterate through all the pages stored above.
                              print(f"Generating images for {book_name}")
                              images_from_path = convert_from_path(path, dpi=70, output_folder=f'{root}/ocr_output')

                              for page_number, page in enumerate(images_from_path):
                                        # Declaring filename for each page of PDF as JPG. For each page, filename will be: PDF page n -> page_n.jpg"""

                                        print(f"Processing {book_name} page {str(page_number)}/{len(images_from_path)}")

                                        os.makedirs(f"{root}/ocr_output/jpeg/{book_name}", exist_ok=True)

                                        filename = f"{root}/ocr_output/jpeg/{book_name}/page_{str(page_number)}.jpg"
                                        # save the image of the page in system

                                        page.save(filename, 'JPEG')
                                        print(f"Saving page into {filename}")
                                        # increment the counter to update filename

                                        # recognize the text as string in image using pytesserct
                                        text = str(((pytesseract.image_to_string(Image.open(filename)))))

                                        page_lines = text.split('\n')

                                        print(f"Parsed {len(page_lines)} lines of text")
                                        print("===")
                                        lines_of_text.extend(page_lines)


extract_text_from_pdf(f"{root}/input")

with open(f'{root}/ocr_parsed_lines.json', 'w+') as f:
          json.dump(lines_of_text, f, indent=2)
