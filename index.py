from openai import OpenAI
import os
import glob
import base64
import requests
import anthropic
from pathlib import Path
from openai import OpenAI
import json
from pathlib import Path

#coucou


client = OpenAI()


def get_description(image):
    """
    This function retrieves a description using the OpenAI API Key.
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Path to your image
    image_path = image

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "peux-tu reconnaitre les personnages présents dans cette image? répond moi avec une structure json donc la clef est 'personnages' et uniquement avec ce JSON stp",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    print(response.json())

    return response.json()["choices"][0]["message"]["content"]


# Get the first image in the current directory
image_files = glob.glob("*.jpg") + glob.glob("*.jpeg") + glob.glob("*.png")
if image_files:
    image = image_files[0]
else:
    raise FileNotFoundError("No image files found in the current directory.")

# personnages = get_description(image)
# print(personnages)


def create_story():
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=os.environ.get("CLAUDE_API_KEY"),
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        temperature=1,
        system="You are an AI assistant with a passion for creative writing and storytelling. Your task is to collaborate with users to create engaging stories, offering imaginative plot twists and dynamic character development. Encourage the user to contribute their ideas and build upon them to create a captivating narrative.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Let's create a story about a young woman named Lila who discovers she has the power to control the weather. She lives in a small town where everyone knows each other.",
                    }
                ],
            }
        ],
    )
    print(message.content)


# Call the function
# create_story()

# "met dans le peau d'un storyteller, peux-tu créer une histoire, un dialogue ramboleques avec ces trois personnages de dessin animé { "personnages": ["Bibou", "Yoyo", "Gluglu"]}", repons moi avec cette structure xml <perso></perso><dialogue></dialogue>"
import xml.etree.ElementTree as ET


def parse_story(xml_content):
    root = ET.fromstring(f"<root>{xml_content}</root>")
    story = []
    current_perso = None

    for elem in root.iter():
        if elem.tag == "perso":
            current_perso = elem.text
        elif elem.tag == "dialogue" and current_perso:
            story.append({"perso": current_perso, "dialogue": elem.text})
            current_perso = None

    return story


xml_content = """
<perso>Bibou</perso>
<dialogue>Mes amis, j'ai une idée fantastique ! Et si on construisait une machine à voyager dans le temps avec des morceaux de fromage et des plumes de paon ?</dialogue>
<perso>Yoyo</perso>
<dialogue>Oh, Bibou ! Tu as toujours des idées si farfelues ! Mais... ça pourrait être amusant. Où trouverons-nous autant de fromage ?</dialogue>
<perso>Gluglu</perso>
<dialogue>J'ai une meilleure idée ! Utilisons des bulles de savon géantes et des chaussettes dépareillées. C'est bien connu, les chaussettes disparaissent toujours mystérieusement. Elles doivent donc avoir des pouvoirs magiques !</dialogue>
<perso>Bibou</perso>
<dialogue>Gluglu, tu es un génie ! Ajoutons aussi des moustaches de chat pour la navigation temporelle. Yoyo, tu pourrais nous tricoter une antenne en spaghettis ?</dialogue>
<perso>Yoyo</perso>
<dialogue>Tricoter des spaghettis ? Mais c'est impossible ! ... Oh, et puis zut, dans notre monde tout est possible ! Je vais chercher mes aiguilles à tricoter en gelée !</dialogue>
<perso>Gluglu</perso>
<dialogue>Et moi, je vais capturer des rires d'enfants dans des bocaux. On ne sait jamais, ça pourrait alimenter notre machine !</dialogue>
<perso>Bibou</perso>
<dialogue>Parfait ! Rendez-vous dans une heure avec tous nos ingrédients magiques. Nous allons créer la machine à voyager dans le temps la plus loufoque de tous les univers !</dialogue>
<perso>Yoyo</perso>
<dialogue>J'espère qu'on ne va pas atterrir dans le ventre d'une baleine qui chante de l'opéra...</dialogue>
<perso>Gluglu</perso>
<dialogue>Ce serait génial ! On pourrait lui apprendre à danser le moonwalk !</dialogue>
<perso>Bibou</perso>
<dialogue>En avant, mes amis ! L'aventure la plus farfelue de notre vie nous attend !</dialogue>"""

# xml_content = """
# <perso>Bibou</perso>
# <dialogue>Mes amis, j'ai une idée fantastique ! Et si on construisait une machine à voyager dans le temps avec des morceaux de fromage et des plumes de paon ?</dialogue>
# <perso>Yoyo</perso>
# <dialogue>Oh, Bibou ! Tu as toujours des idées si farfelues ! Mais... ça pourrait être amusant. Où trouverons-nous autant de fromage ?</dialogue>
# <perso>Gluglu</perso>
# <dialogue>J'ai une meilleure idée ! Utilisons des bulles de savon géantes et des chaussettes dépareillées. C'est bien connu, les chaussettes disparaissent toujours mystérieusement. Elles doivent donc avoir des pouvoirs magiques !</dialogue>
# """


parsed_story = parse_story(xml_content)
story_json = json.dumps(parsed_story, ensure_ascii=False, indent=4)
print(story_json)


def generate_audio_from_story(story_json):
    voices = {"Bibou": "nova", "Yoyo": "alloy", "Gluglu": "shimmer"}

    story_list = json.loads(story_json)
    for index, entry in enumerate(story_list):
        perso = entry["perso"]
        dialogue = entry["dialogue"]
        voice = voices.get(perso, "default_voice")

        speech_file_path = Path(__file__).parent / f"{index}_speech_{perso}.mp3"
        response = client.audio.speech.create(
            model="tts-1", voice=voice, input=dialogue
        )

        response.stream_to_file(speech_file_path)


# Example usage
# story_json = [
#     {
#         "perso": "Bibou",
#         "dialogue": "Mes amis, j'ai une idée fantastique ! Et si on construisait une machine à voyager dans le temps avec des morceaux de fromage et des plumes de paon ?"
#     },
#     {
#         "perso": "Yoyo",
#         "dialogue": "Oh, Bibou ! Tu as toujours des idées si farfelues ! Mais... ça pourrait être amusant. Où trouverons-nous autant de fromage ?"
#     },
#     {
#         "perso": "Gluglu",
#         "dialogue": "J'ai une meilleure idée ! Utilisons des bulles de savon géantes et des chaussettes dépareillées. C'est bien connu, les chaussettes disparaissent toujours mystérieusement. Elles doivent donc avoir des pouvoirs magiques !"
#     },
#      {
#         "perso": "Bibou",
#         "dialogue": "Genial aurelien"
#     },
# ]

generate_audio_from_story(story_json)
