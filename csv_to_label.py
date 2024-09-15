from jinja2 import Template
import barcode
from barcode.writer import ImageWriter
import imgkit
import os
import csv


# Get the directory of the running script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the wkhtmltoimage executable on your system
wkhtmltoimage_path = '/usr/bin/wkhtmltoimage'  # Update with the correct path if necessary


# Define fields to update in the HTML label
product = 'Product A'
date = '2025-10-15'
position = 'A1'
barcode_class = 'ean13'
barcode_value = '1234567890128'
barcode_path = os.path.join(script_dir, 'temp_barcode')  # Absolute path to barcode image
html_path = os.path.join(script_dir, 'temp_label.html')  # Absolute path to output HTML file

# Paths for input and output
csv_path = os.path.join(script_dir, 'labels.csv')
template_path = os.path.join(script_dir, 'label_template.html')
output_dir = os.path.join(script_dir, 'output')
# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def generate_label(product, date, position, barcode_class, barcode_value):
    template_path = os.path.join(script_dir, 'label_template.html')  # Absolute path to barcode image
    output_path=os.path.join(script_dir, f'output/{barcode_value}.png')

    # Read HTML template file
    with open(template_path, 'r') as file:
        template_content = file.read()

    # Create a Jinja2 template object
    template = Template(template_content)

    # Generate barcode image
    ean = barcode.get_barcode_class(barcode_class)
    barcode_instance = ean(barcode_value, writer=ImageWriter())
    barcode_instance.save(barcode_path)
 
    # Render the template with field values and barcode image
    rendered_html = template.render(product=product, date=date, position=position, barcode="barcode_path")

    # Write the updated HTML content to a temporary file
    with open(html_path, 'w') as temp_file:
        temp_file.write(rendered_html)



    # Options for imgkit
    options = {
        'enable-local-file-access': '',
        'load-error-handling': 'ignore',
        'width': '400',
        'height': '500',
        'disable-smart-width': '',
        'quality': '100',
        # 'crop-h': '100'  # Adjust height as needed to make sure content isn't clipped
    }

    # Configure imgkit with the path to the wkhtmltoimage executable and additional options
    config = imgkit.config(wkhtmltoimage=wkhtmltoimage_path)


    # Convert the HTML file to a PNG image
    imgkit.from_file(html_path, output_path, config=config, options=options)


def process_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            generate_label(row['product'], row['date'], row['position'], row['barcode_class'], row['barcode_value'])

# Read the CSV and generate labels for each row
process_csv(csv_path)

# Remove the temporary HTML file
try:
    if os.path.exists(html_path):
        os.remove(html_path)
        print(f"Temporary file {html_path} removed successfully.")
    if os.path.exists(f"{barcode_path}.png"):
        os.remove(f"{barcode_path}.png")
        print(f"Temporary file {barcode_path}.png removed successfully.")
except Exception as e:
    print(f"Error occurred while removing the temporary file: {e}")