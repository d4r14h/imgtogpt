import pytesseract, openai, requests, tempfile, json, os
from PIL import Image
from simple_term_menu import TerminalMenu

if os.path.isfile("./apiKey.txt"):
    with open("apiKey.txt", "r+") as keyFile:
        contents = keyFile.read()
        openai.api_key = contents
else:
    print("Looks like you don\'t have an API Key yet!")
    with open("apiKey.txt", "r+") as keyFile:
        keyFile.write(input("Enter your OpenAI API Key:\n>>> "))
        contents = keyFile.read()
        openai.api_key = contents

# Set the path to the Tesseract binary
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
srcTypes = ["URL", "FilePath"]

srcType = TerminalMenu(srcTypes, title="Select Source Image Method:\n")
srcType_index = srcType.show()


def determineSrcType(pathType):
    global url
    if pathType == "URL":
        url = input("Enter the Image URL:\n>>> ")
    elif pathType == "FilePath":
        url = input("Enter the Image File Path:\n>>> ")


determineSrcType(srcTypes[srcType_index])


response = requests.get(url)
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(response.content)
        img = f.name

extracted_text = pytesseract.image_to_string(img)
print(extracted_text)

engines = openai.Engine.list()

data = json.loads(str(engines))
ids = [element['id'] for element in data['data']]
terminal_menu = TerminalMenu(ids, title="Select your preferred AI Engine:\n")
menu_entry_index = terminal_menu.show()
print(f"You have selected {ids[menu_entry_index]}!")
completion = openai.Completion.create(engine=ids[menu_entry_index], prompt=extracted_text, max_tokens=1500, frequency_penalty=0.08)

print(completion.choices[0].text)

