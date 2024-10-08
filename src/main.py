import json

import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.responses import PlainTextResponse

from create_user import CreateUser
from custom_exceptions import ConflictException, NotFoundException, MissingFieldException, WrongDataTypeException
from delete_user import DeleteUser
from get_user import GetUser


class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=5, max_length=50)


app = FastAPI(debug=True)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exception_type = repr(exc.errors()[0]["type"])
    if "_type" in exception_type or "missing" in exception_type:
        return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)
    return PlainTextResponse(str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


router = APIRouter()


@router.post("/users")
def create_user_route(user: User) -> Response:
    create_user = CreateUser()
    headers = {"Content-Type": "application/json"}
    try:
        created_user = create_user.execute(user.model_dump())
        content = json.dumps(created_user)
        headers["Location"] = f"/api/users/{created_user['id']}"
        response = Response(content, status.HTTP_201_CREATED, headers)
    except (MissingFieldException, WrongDataTypeException) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e), headers)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e), headers)
    except ConflictException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e), headers)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), headers)
    return response


@router.get("/users/{user_id}")
def get_user_route(user_id: int) -> Response:
    get_user = GetUser()
    headers = {"Content-Type": "application/json"}
    try:
        fetched_user = get_user.execute(user_id)
        content = json.dumps(fetched_user)
        response = Response(content, status.HTTP_200_OK, headers)
    except NotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e), headers)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), headers)
    return response


@router.delete("/users/{user_id}")
def delete_user_route(user_id: int) -> Response:
    headers = {"Content-Type": "application/json"}
    delete_user = DeleteUser()
    try:
        delete_user.execute(user_id)
        response = Response(None, status.HTTP_204_NO_CONTENT, headers)
    except NotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e), headers)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), headers)
    return response


app.include_router(router, prefix="/api")


def main() -> None:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == '__main__':
    main()
