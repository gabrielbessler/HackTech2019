# Dependencies:
# Tesseract OCR 4.0 (for pytesseract)
# Poppler (for pdf2image) (Ubuntu preinstalled)
# PIL 

# Can also use numpy and cv2 images :)
from PIL import Image
# Dope OCR library wrapper
import pytesseract as tes
# Requires Poppler dependency (or not?)
import pdf2image
import os
import io

# Gabe sends me stuff base64 encoded cause javascript
import base64


# A bunch of wrappers to avoid having to lookup tesseract docs

def read_image(filename):
	'''Returns an Image object opened from the file.
	Uses PIL under the hood atm.'''
	return Image.open(filename)


def get_string(image, lang=None, debug=False, filename="test", postprocess=False):
	'''Returns raw string of file.'''
	if lang:
		output_string = tes.image_to_string(image, lang=lang)
	else:
		output_string = tes.image_to_string(image)
	
	if postprocess:
		output_string = postprocessing(output_string)
	
	if debug:
		if not os.path.isdir('output_string'):
			try:
				os.mkdir('output_string')
			except:
				print("Error creating directory for string output")
		with open('output_string/'+filename+'.txt', 'w') as f:
			f.write(output_string)
	
	return output_string


def get_bounding_box(image):
	'''Returns tesseracts bounding box notation stuff.
	TODO parse it and show it nicely (I can dream right)'''
	return tes.image_to_boxes(image)

def convert_to_images(filename):
	'''Takes a pdf file and returns a list of PIL Images,
	One Image per page of the PDF.
	Note, will not raise exception and will return an empty list for error.'''
	# Also note, can take raw bytes and convert using
	# convert_from_bytes
	## Supposedly png is slower than jpeg here
	return pdf2image.convert_from_path(filename)

def create_readable_pdf(image, filename='test', debug=True):
	'''Runs OCR on an image and returns a string containing the PDF data.
	Also writes the pdf to output_pdf directory.'''
	pdf = tes.image_to_pdf_or_hocr(image, extension='pdf')
	
	if debug:
		if not os.path.isdir('output_pdf'):
			try:
				os.mkdir('output_pdf')
			except:
				print("Error creating directory for pdf output")
		with open('output_pdf/'+filename+'.pdf', 'wb') as f:
			f.write(pdf)
	
	return pdf

def create_readable_hocr(image, filename='test', debug=True):
	'''Runs OCR on an image and returns a string containing the HOCR data.
	Also writes the HOCR to output_hocr directory.'''
	hocr = tes.image_to_pdf_or_hocr(image, extension='hocr')
	
	if debug:
		if not os.path.isdir('output_hocr'):
			try:
				os.mkdir('output_hocr')
			except:
				print("Error creating directory for hocr output")
		with open('output_hocr/'+filename+'.html', 'wb') as f:
			f.write(hocr)
	
	return hocr


def postprocessing(text):
	'''Takes the string output of OCR and runs some processing to improve it.'''
	
	# Look for word splits across lines with a '-' and rejoin the words
	text = text.replace('-\n', '')
	
	# Split by double next line for paragraphs and replace single newlines with a space
	t = text.split('\n\n')
	t = map(lambda x: x.replace('\n', ' '), t)
	text = '\n\n'.join(t)
	
	return text


def process_IMG(base64_image):
	'''Function call for Gabe.
	Takes in a base64 string.
	Outputs the OCR string contained in the image.'''
	# Step 1, decode the base 64 image
	image_data = base64.b64decode(base64_image)
	# Convert to a PIL Image object
	image = Image.open(io.BytesIO(image_data))
	# Process the OCR and apply  postprocessing
	output = get_string(image, postprocess=True)
	return output

def process_PDF(base64_PDF):
	'''Function call for Gabe.
	Takes in a base64 string of a pdf.
	Outputs the OCR contained in the pdf'''
	# Start by passing the pdf data into an image generator
	pdf_data = base64.b64decode(base64_PDF)
	#filename = "temp.pdf"
	#with open(filename, 'wb') as f:
	#	f.write(pdf_data)
	images = pdf2image.convert_from_bytes(pdf_data)
	output = map(lambda x: get_string(x, postprocess=True), images)
	return ' '.join(output)

def PDFFromBase64(base64_image):
	'''Function call for Gabe.
	Takes image data and outputs a base64 encoded pdf.'''
	image_data = base64.b64decode(base64_image)
	image = Image.open(io.BytesIO(image_data))
	pdf = create_readable_pdf(image, debug=False)
	return base64.b64encode(pdf)
	
	
	
# Common errors:
#----------------
# bullet points and similar object being recognized as letters
# Could do a check for single letters followed by capital, starting sentence
# Improper spacing around math equations
#
	
	
	
#def test():
#	images = convert_to_images('hw5Description.pdf')
#	text = map(get_string, images)
#	return ''.join(text)