import os
import re
from dotenv import load_dotenv
from set_recognizer import find_sets_from_data, get_cards_from_image, find_set_indices
from output_processing import highlight_cards_by_id
import argparse
from PIL import Image 

def process_image(image_path, filename, output_folder):
    load_dotenv()
    azure_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OAI_KEY")

    # Find cards on image
    board_df = get_cards_from_image(image_path, azure_endpoint, azure_key)

    # Find sets
    sets = find_sets_from_data(board_df)

    # Return output
    if sets:
        print("Set(s) found.")
        for i, set_dict in enumerate(sets):
            processed_filename = f"analyzed_set-{i+1}_{filename}"
            output_path = f"{output_folder}/{processed_filename}"

            set_indices = find_set_indices(board_df, set_dict)
            highlight_cards_by_id(image_path, set_indices, output_path)
        
        # TODO return all images
        return processed_filename
    else:
        print("No sets found.")
        # Save image unmodified
        processed_filename = f"analyzed_no-set_{filename}"
        output_path = f"{output_folder}/{processed_filename}"
        img = Image.open(image_path)
        img.save(output_path)

        return processed_filename


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, help="Path to input image")
    args = parser.parse_args()
    image_path = args.image_path
    print(f"Analyzing {image_path}")

    filename = re.search(r"/([^/]+)\.jpg", image_path).group(1)
    filename += ".jpg"

    process_image(image_path, filename, output_folder="output/")