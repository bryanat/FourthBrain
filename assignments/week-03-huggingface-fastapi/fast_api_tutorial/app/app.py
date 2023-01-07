from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from typing import List

# Load transformers translation model reference in local directory (localModels/)
pipeline_en_to_fr = pipeline("translation_en_to_fr", model="localModels/EnglishToFrenchTranslator")
pipeline_en_to_de = pipeline("translation_en_to_de", model="localModels/EnglishToGermanTranslator")
pipeline_en_to_ro = pipeline("translation_en_to_ro", model="localModels/EnglishToRomanianTranslator")

class TranslateText(BaseModel):
    translate_text: str
    language_code: str

class TranslateTexts(BaseModel):
    translate_texts: List[str]
    language_code: str

# fastapi server
app = FastAPI()

# index / root endpoint
@app.get("/")
async def index():
    return {"data": "Hello World", "log": "/ route hit"}

# not really how it works :)
@app.get("/signout")
async def signout():
    return {"data": "Goodbye World!", "log": "/signout route hit"}

########################Non-Pydantic Routes##################################
# Route to echo
@app.post("/echo/{message}")
async def echo(message: str):
    return {"data": f"echo: {message}", "log": f"/echo/{message} route hit"}

# Route to translate english
@app.post("/translate/{language_code}/{translate_text}")
async def translate(language_code: str, translate_text: str):
    # match route to desired output language translation
    if language_code == "fr":
        output_text = pipeline_en_to_fr([translate_text])
    elif language_code == "de":
        output_text = pipeline_en_to_de([translate_text])
    elif language_code == "ro":
        output_text = pipeline_en_to_ro([translate_text])
    else:
        output_text = f"Language translation for en to {language_code} currently not supported, supported languages are English to: French, German, Romanian"
    
    ## match syntax not supported until py3.10, currenty using py3.9
    # match language_code:
    #     case "fr":
    #         output_text = pipeline_en_to_fr([english_text])
    #     case "de":
    #         output_text = pipeline_en_to_de([english_text])
    #     case "ro":
    #         output_text = pipeline_en_to_ro([english_text])
    #     case _:
    #         output_text = f"language translation for en to {language_code} currently not supported, supported languages are English to: French, German, Romanian"
    return {"data": output_text, "log": f"/translate/{language_code}/{translate_text} route hit"}
#############################################################################


##########################Pydantic Routes####################################
# routes below return the same as above, but using pydantic models for parsing

# Route to echo using pydantic models
@app.post("/pydantic-echo")
async def pydantic_echo(req: TranslateText):
    return {"data": f"echo: {req.translate_text}", "log": f"/echo/{req.translate_text} route hit"}

# Route to translate english using pydantic models
@app.post("/pydantic-translate")
async def translate(req: TranslateText):
    # match route to desired output language translation
    if req.language_code == "fr":
        output_text = pipeline_en_to_fr([req.translate_text])
    elif req.language_code == "de":
        output_text = pipeline_en_to_de([req.translate_text])
    elif req.language_code == "ro":
        output_text = pipeline_en_to_ro([req.translate_text])
    else:
        output_text = f"Language translation for en to {req.language_code} currently not supported, supported languages are English to: French, German, Romanian"
    return {"data": output_text, "log": f"/translate/{req.language_code}/{req.translate_text} route hit"}

# used to launch uvicorn by running filename.py (python3 app.py) in local app folder 
@app.post("/batch-translate")
def batch_translate(req: TranslateTexts):
    batch_pipeline = type(pipeline)
    if req.language_code == "fr":
        batch_pipeline = pipeline_en_to_fr
    elif req.language_code == "de":
        batch_pipeline = pipeline_en_to_de
    elif req.language_code == "ro":
        batch_pipeline = pipeline_en_to_ro
    # # default to french, but should be replaced with error handling, too lazy.
    # else:
    #     batch_pipeline = pipeline_en_to_fr
    else: 
        return {"data": f"Your request cannot be translated from en to {req.language_code}", "log": f"/batch-translate/ route hit with unhandled language_code: {req.language_code}"}
    results = []
    for translate_text in req.translate_texts:
        results.append(batch_pipeline(translate_text))
    return {"data": results, "log": "/batch-translate/ route hit"}
#############################################################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
