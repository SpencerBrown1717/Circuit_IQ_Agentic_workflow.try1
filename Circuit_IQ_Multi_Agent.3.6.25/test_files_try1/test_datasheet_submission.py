import requests
import json

# Test datasheet content
datasheet_content = """
PCB Specifications:
- Copper Layer Thickness: 1oz copper on top and bottom layers
- Soldermask: Green soldermask on both sides
- Silkscreen: White silkscreen on top layer
- Drill Specifications: 0.3mm minimum hole size
"""

# Create test files
with open('test_datasheet.txt', 'w') as f:
    f.write(datasheet_content)

# Example Gerber content
gerber_content = "G04 Test Gerber File*\n%FSLAX36Y36*%\n%MOMM*%"

with open('copper_top.gbr', 'w') as f:
    f.write(gerber_content)

# Submit files
files = {
    'datasheet': ('datasheet.txt', open('test_datasheet.txt', 'rb')),
    'gerber_files': ('copper_top.gbr', open('copper_top.gbr', 'rb'))
}

response = requests.post(
    'http://localhost:8000/submit-datasheet',
    files=files
)

print(response.json()) 