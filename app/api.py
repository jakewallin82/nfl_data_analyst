from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse

from app.models import QuestionRequest
from app.langchain_config import generate_code_solution

import os

router = APIRouter()

@router.post("/generate-code")
async def generate_code(request: QuestionRequest):
    question = request.question
    print('generating code')
    solution = generate_code_solution(question)

    # Write the generated code to a file
    script_dir = os.path.dirname(__file__)
    code_file_path = os.path.join(script_dir, 'example_code.py')
    with open(code_file_path, 'w') as file:
        file.write(solution.imports + '\n' + solution.code)

    # Execute the generated code
    print("running code")
    local_vars = {}
    example_code = solution.imports + '\n' + solution.code
    try:
        exec(example_code, {}, local_vars)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error executing code: {e}")

    generated_filename = local_vars.get('generated_filename', 'none')
    return {"filename": generated_filename}

@router.get("/output")
async def get_output(filename: str):
    script_dir = os.path.dirname(__file__)
    # Assuming the image is saved as 'output.png' (modify as necessary)
    file_path = os.path.join(script_dir, 'content', filename)

    if filename.endswith(".png"):
        return FileResponse(file_path, media_type="image/png", filename=filename)
    elif filename.endswith(".csv"):
        try:
            df = pd.read_csv(file_path)
            data = df.to_dict(orient='records')
            return JSONResponse(content=data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading CSV file: {e}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
