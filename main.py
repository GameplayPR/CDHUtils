from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse

import json

from scripts.json_to_excel import convert_json_to_excel
from scripts.pdf_to_image import convert_pdf_to_image

app = FastAPI(title="CDH Utils API")

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

@app.post("/pdf_to_image")
async def pdf_to_image_endpoint(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo enviado não é um PDF.")

    try:
        pdf_bytes = await file.read()
        png_images_base64 = convert_pdf_to_image(pdf_bytes)

        return JSONResponse(content={"images": png_images_base64})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5125, reload=True)
