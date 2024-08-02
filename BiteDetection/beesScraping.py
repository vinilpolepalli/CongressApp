import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO

# Function to download images from a single page
def download_images_from_page(url, specific_folder, start_index):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tags = soup.find_all('img')
    image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

    for i, img_url in enumerate(image_urls):
        try:
            full_url = img_url if img_url.startswith('http') else f"https://www.example.com{img_url}"
            img_response = requests.get(full_url)
            img = Image.open(BytesIO(img_response.content))
            img = img.convert("RGB")  # Convert to RGB format
            img.save(os.path.join(specific_folder, f'bee_sting_{start_index + i}.jpg'), 'JPEG')
            print(f"Downloaded {full_url}")
        except Exception as e:
            print(f"Could not download {img_url}: {e}")

# Main script
base_url = "https://www.google.com/search?sca_esv=8a21897d5a918d7d&q=bee+sting+red+mark&uds=ADvngMjIlLeH6JmF8XYRfQNKteaQTQ8MXIlUsrrKJ-Y1sY58OStmBxW4TLP3CEhSnSeIOFFIhEUvgg_lAO7ciSsUXHe4MhWZbsZJfy9e2Gpk3-fRdn9XG7vj1aelx5Ux87meKVly3Iz_&udm=2&sa=X&ved=2ahUKEwiCos_jmdeHAxVSEVkFHQ3fHpUQxKsJegQIEhAB&ictx=0&biw=1275&bih=842&dpr=2&start="  # Replace with the actual URL
specific_folder = '/Users/vinil_polepalli/Desktop/bee-stings'  # Replace with your desired folder path
os.makedirs(specific_folder, exist_ok=True)

# Determine the starting index based on existing files
existing_files = os.listdir(specific_folder)
existing_indices = [int(f.split('_')[-1].split('.')[0]) for f in existing_files if f.startswith('bee_sting_') and f.endswith('.jpg')]
start_index = max(existing_indices) + 1 if existing_indices else 0

num_pages = 5  # Number of pages to scrape
images_per_page = 20  # Approximate number of images per page

for page in range(num_pages):
    page_start_index = start_index + page * images_per_page
    page_url = f"{base_url}{page_start_index}"
    download_images_from_page(page_url, specific_folder, page_start_index)

print("Image download complete.")