from fastapi import HTTPException

class InvalidTemplateError(HTTPException):
    def __init__(self,detail:str = "Please provide a valid template. "):
        super().__init__(status_code = 404,detail = detail)