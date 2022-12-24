from fastapi import FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# start fastapi server with !python3 app.py as magic __name__ will resolve to uvicorn main:app.py
app = FastAPI()

# all get requests rn just so I can test in webbrowser without postman or fastapi/docs
@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/signout")
async def signout():
    return {{"message": "Goodbye World!"}}

@app.get("/echo/{message}")
async def ekko(message: str):
    return {"echo": message}

@app.get("/ekko/{message}")
async def ekko(message: str):
    return {"ekko": f"ekkooo: {message}"}

@app.get("/en-to-fr-model/{inputEN}")
async def translate():
    # outputFR = return from EnFrTranslationPipeline
    return {{"input-EN": inputEN}, {"output-FR": outputFR}}
    
