import requests
import os

def download_file(relative_path, destination_folder):
    """
    Downloads a file from the specified path relative to https://naif.jpl.nasa.gov/pub/naif/
    
    Args:
        relative_path (str): Path to the file relative to https://naif.jpl.nasa.gov/pub/naif/
        destination_folder (str): Folder where the file should be saved, relative to the script's location
    
    Returns:
        str: Path to the downloaded file
    """
    
    # Base URL
    base_url = "https://naif.jpl.nasa.gov/pub/naif/"
    file_url = os.path.join(base_url, relative_path)
    
    # Determine the full destination path relative to the script's location
    script_directory = os.path.dirname(os.path.abspath(__file__))
    full_destination_folder = os.path.join(script_directory, destination_folder)
    
    # Check if the destination folder exists; create it if not
    os.makedirs(full_destination_folder, exist_ok=True)
    
    # Path to save the file
    file_name = os.path.basename(relative_path)
    destination_path = os.path.join(full_destination_folder, file_name)
    
    try:
        # Download the file
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        
        # Save the file
        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded file: {destination_path}")
        return destination_path
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")
        return None
    