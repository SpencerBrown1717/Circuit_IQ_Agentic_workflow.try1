import requests
import time
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URL of the Boss Agent
BASE_URL = "http://localhost:8000"

def create_test_file(content, filename):
    """Create a test file with proper filename"""
    return (filename, content.encode('utf-8'), 'application/octet-stream')

# Example Gerber file content
test_gerber_content = """G04 Test Gerber File*
%FSLAX36Y36*%
%MOMM*%
%SFA1.0B1.0*%
G04 End of header*
M02*"""

def test_gerber_submission():
    # Create test files with proper filenames
    files = {
        'copper_top': create_test_file(test_gerber_content, 'copper_top.gbr'),
        'copper_bottom': create_test_file(test_gerber_content, 'copper_bottom.gbr'),
        'soldermask_top': create_test_file(test_gerber_content, 'soldermask_top.gbr'),
        'drill': create_test_file(test_gerber_content, 'drill.xln')
    }

    try:
        # Submit job
        logger.info("Submitting job...")
        response = requests.post(f"{BASE_URL}/submit", files=files)
        response.raise_for_status()
        job_data = response.json()
        job_id = job_data['job_id']
        logger.info(f"Job submitted. Job ID: {job_id}")

        # Monitor status
        max_attempts = 5
        for attempt in range(max_attempts):
            logger.info(f"Checking status (attempt {attempt + 1}/{max_attempts})...")
            status_response = requests.get(f"{BASE_URL}/status/{job_id}")
            status_response.raise_for_status()
            status_data = status_response.json()
            logger.info(f"Status: {status_data}")
            
            if status_data['status'] in ['completed', 'failed']:
                break
                
            time.sleep(2)

        # Try to download if job completed
        if status_data['status'] == 'completed':
            logger.info("Downloading results...")
            download_response = requests.get(f"{BASE_URL}/download/{job_id}")
            if download_response.status_code == 200:
                output_file = Path(f"gerber_files_{job_id}.zip")
                output_file.write_bytes(download_response.content)
                logger.info(f"Results downloaded to {output_file}")
            else:
                logger.error(f"Download failed: {download_response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during test: {e}")
        raise

def test_datasheet_submission():
    """Test submitting a datasheet"""
    test_datasheet = """
    Board Specifications:
    - Dimensions: 100mm x 100mm
    - Copper layers: 2 layers, 1oz copper thickness
    - Soldermask: Green, both sides
    - Silkscreen: White, top side only
    - Drill: Min hole size 0.3mm
    """

    try:
        files = {
            'datasheet': ('specs.txt', test_datasheet.encode('utf-8'), 'text/plain')
        }
        
        logger.info("Submitting datasheet...")
        response = requests.post(f"{BASE_URL}/submit-datasheet", files=files)
        response.raise_for_status()
        result = response.json()
        logger.info(f"Datasheet submission result: {result}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during datasheet test: {e}")
        raise

if __name__ == "__main__":
    test_gerber_submission()
    test_datasheet_submission() 