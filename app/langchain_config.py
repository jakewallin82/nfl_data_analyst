import nfl_data_py as nfl
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel as LangchainBaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class CodeOutput(LangchainBaseModel):
    prefix: str = Field(description="Description of the problem and approach", default="")
    imports: str = Field(description="Code block import statements", default="")
    code: str = Field(description="Code block not including import statements", default="")
    description: str = Field(default="Schema for code solutions to questions about NFL Data")

expt_llm = "gpt-4o"
llm = ChatOpenAI(temperature=0, model=expt_llm)

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'column-descriptions.csv')
with open(file_path, 'r') as file:
    context = file.read()

code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a coding assistant with expertise in using the nfl_data_py library, a Python library for analyzing National Football League data. There is a large dataset of play-by-play data that you will be analyzing.
            You will receive a list of the column keys and a description and datatype for each of the columns. You must use these descriptions as well as common knowledge of the NFL football rules to craft logical code to analyze the dataset.
            Sometimes you will have to import external libraries to generate the requests, but most of the analysis can come from transforming the data. You cannot assume that a column key exists, You must look at the provided context to figure out which column key must be used to correctly process the data.
            Each of the questions asked can be solved using only columns described in the dataset. In the description, provide reasoning for why you use each column.

            Before generating the functioning code block, you must provide a description of the code solution, and a list of imports.
            Here are instructions for the 3rd piece of output: the functioning code block:

            Preceding each import of a 3rd party module, you must include:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

            Each file must contain the following:
            import nfl_data_py as nfl
            import os

            nfl.import_pbp_data([2023])  #This is how you load the data

            The output file path must also be app/content, and the output should have a representative and unique name.

            The code must have the following line, so we can keep track of the new file's name (must be csv or png):

            generated_filename = SOME_REPRESENTATIVE_FILE_NAME.csv

            
            If asked to generate a plot, the file must not use plt.show(), but instead must end with plt.savefig(output_file_path)

            ------- 
            {context}
            ------- 
            Answer the above provided documentation. Ensure any code you provide can be executed with all required imports and variables defined. 
            Structure your answer with a description of the code solution. The example code is provided as a Jupyter notebook, but you should output an executable Python file.
            Then list the imports. And finally list the functioning code block. Make sure to terminate each string, and return the data in proper format. Here is the user question:""",
        ),
        ("placeholder", "{messages}"),
    ]
)

code_gen_chain = code_gen_prompt | llm.with_structured_output(CodeOutput)

def generate_code_solution(question: str) -> CodeOutput:
    return code_gen_chain.invoke({"context": context, "messages": [("user", question)]})
