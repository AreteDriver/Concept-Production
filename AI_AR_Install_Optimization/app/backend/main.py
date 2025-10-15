from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "AI_AR_Install_Optimization online"}
