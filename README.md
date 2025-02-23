# Mistral-DesktopApp
Streamlit Chat-bot with Mistral.ai free API into a standalone Windows Desktop App

## Instructions

- Clone the repo

- create the virtual environment
```bash
python -m venv venv
```
- activate the virtual environment
```bash
.\venv\Scripts\activate
```
- Install the dependencies
```bash
pip install streamlit mistralai streamlit-desktop-app
```
- from the terminal with the venv activated, run
```bash
streamlit-desktop-app.exe build .\MistralREMOTE.py --name Mistral_Desktop  --pyinstaller-options --onefile --collect-all streamlit --hidden-import mistralai --add-data user.png:. --add-data assistant.png:. -i .\assistant.ico --hidden-import PIL --add-data mistralai.png:. --add-data mistral-banner.png:.
```

Two new sub-directory will be created:
- build (building files)
- dist (our `.exe` file will be here


### The building process
<img src='https://github.com/fabiomatricardi/Mistral-DesktopApp/raw/main/st-DeskApp-create_SM.gif' width=950>

### Running the App
<img src='https://github.com/fabiomatricardi/Mistral-DesktopApp/raw/main/st-DeskApp-run.gif' width=950>
