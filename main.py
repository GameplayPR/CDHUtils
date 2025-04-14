from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
from scripts.json_to_excel import convert_json_to_excel

app = FastAPI(title="json_to_excel")

@app.post("/json_to_excel")
async def json_to_excel_endpoint(request: Request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Corpo da requisição não é um JSON válido.")

    try:
        excel_file = convert_json_to_excel(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=converted.xlsx"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5125, reload=True)
