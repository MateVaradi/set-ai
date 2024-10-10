import base64
import pandas as pd
import itertools
from openai import AzureOpenAI
import os

MODEL="gpt-4o"

PROMPT = """Please describe all the cards that are on the following image. Go from left to right, top to bottom. 

Each card has four characteristics: shape, color, number and shading. 

Shape describes the shape(s) on the card, this can be a diamond, a squiggle or an oval. 

Number describes how many shapes there are on the card. Color describes the color of the shapes.

Shading describes whether the shapes are fully filled with color (solid), or not filled at all and are white in the middle (outlined). 
A third shading option is striped, in which case the shape is shaded with narrow parrallel lines in the middle. 
This may appear as being filled with a lighter color. 

The descriptions should be returned as follows:
shape: oval, diamond or squiggle
color: red, green or purple
number: 1, 2 or 3
shading: solid, striped or outline

The output should be organized in a list of dictionaries, where each card's information is given in a dictionary. Such as:
[{"shape": "squiggle", "color": "red", "number": 1, "shading: outline"},
{"shape": "oval", "color": "purple", "number": 3, "shading: striped"}]
Only return the desired output, nothing else."""

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_cards_from_image(image_path, azure_endpoint, api_key, api_version="2024-02-15-preview"):

    base64_image = encode_image(image_path)

    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
            azure_endpoint = azure_endpoint,
            api_key=api_key,  
            api_version=api_version #  Target version of the API, such as 2024-02-15-preview
            )

    # Analyze image with OpenAI
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs responses in the desired format."},
            {"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )

    # Process response
    cards_dict = eval(response.choices[0].message.content.replace("\n","").replace(" ",""))
    cards_df = pd.DataFrame(cards_dict)

    return cards_df


def is_set(triplet):
    set = True
    for c in triplet.columns:
        n = triplet[c].nunique()
        set = set & ((n==1) | (n==3))
        if not set:
            break
    return set
    

def get_all_triplets(board):
    combinations = list(itertools.combinations(board.index, 3))
    triplets = [board.loc[list(comb)] for comb in combinations]
    return triplets


def find_sets_from_data(board):
    triplets = get_all_triplets(board)
    sets = []
    for triplet in triplets:
        set = is_set(triplet)
        if set:
            triplet_dict = triplet.to_dict("records")
            sets.append(triplet_dict)
    return sets

def find_set_indices(cards_df, set_dict):
    set_df = pd.DataFrame(set_dict)
    matching_indices = cards_df.reset_index().merge(set_df, on=list(set_df.columns), how='inner')['index']
    matching_indices = list(matching_indices)

    return matching_indices
