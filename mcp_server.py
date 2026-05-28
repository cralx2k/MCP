from fastapi import FastAPI
from typing import Any, Dict, List
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI(title="MCP Math & Text Server")

class AddInput(BaseModel):
    a: float = Field(..., description="First number to add")
    b: float = Field(..., description="Second number to add")
    # {"a": 5, "b": "hello"}

class SubtractInput(BaseModel):
    a: float = Field(..., description="Number to subtract from")
    b: float = Field(..., description="Number to subtract")

class ReverseTextInput(BaseModel):
    text: str = Field(..., description="Text to reverse")

@app.get("/tools")
async def list_tools():
    return {
        "tools": [
            {
                "name": "add",
                "description": "Adds two numbers together and returns the sum",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "subtract",
                "description": "Subtracts the second number from the first",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "Number to subtract from"},
                        "b": {"type": "number", "description": "Number to subtract"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "reverse_text",
                "description": "Reverses the order of characters in text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to reverse"}
                    },
                    "required": ["text"]
                }
            }
        ]
    }


@app.post("/tools/add")
async def add_numbers(input_data: AddInput):
    result = input_data.a + input_data.b
    return {
        "content": [
            {
                "type":"text",
                "text": f"The sum of {input_data.a} and {input_data.b} is {result}."
            }
        ]
    }

@app.post("/tools/subtract")
async def subtract_numbers(input_data: SubtractInput):
    result = input_data.a - input_data.b
    return {
        "content": [
            {
                "type":"text",
                "text": f"The difference of {input_data.a} and {input_data.b} is {result}."
            }
        ]
    }


@app.post("/tools/reverse_text")
async def reverse_text(input_data: ReverseTextInput):
    reversed_text = input_data.text[::-1]
    return {
        "content": [
            {
                "type":"text",
                "text": f"Original: {input_data.text}\nReversed: {reversed_text}"
            }
        ]
    }




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)