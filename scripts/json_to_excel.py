from io import BytesIO
import pandas as pd

def convert_json_to_excel(json_data):
    if isinstance(json_data, dict):
        data = [json_data]
    elif isinstance(json_data, list):
        data = json_data
    else:
        raise ValueError("O JSON deve ser um dicionário ou uma lista de dicionários.")

    try:
        df = pd.DataFrame(data)
    except Exception as e:
        raise ValueError(f"Erro ao criar DataFrame: {str(e)}")

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    return output
