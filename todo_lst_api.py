from datetime import timedelta
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Request, Response, encoders
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, OAuth2

from auth import Token, authenticate_user, fakeDB, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, \
    get_current_active_user, get_current_user
from todo import todo_dict, Todo, TodoContent
from user import BaseUser, DBUser, RegistrationUser

# from fastapi_auth_middleware import AuthMiddleware, FastAPIUser
app = FastAPI()


# TODO:Is admin middleware

# app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)

@app.post("/login", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fakeDB, form_data.username, form_data.password)
    print(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=BaseUser)
async def create_user(user: RegistrationUser):
    new_user = DBUser(**dict(user), hashed_password=get_password_hash(user.password))
    fakeDB[new_user.username] = dict(new_user)
    return new_user


@app.get("/users/me", response_model=BaseUser)
async def read_users_me(current_user: BaseUser = Depends(get_current_active_user)):
    return current_user


@app.post("/todos")
async def create_todo(todo_content: TodoContent, current_user: BaseUser = Depends(get_current_user)):
    todo = Todo(**dict(todo_content), owner=current_user.username)
    todo_dict[todo.id] = todo
    return todo


@app.get("/todos")
async def get_all_user_todos(current_user: DBUser = Depends(get_current_user)):
    return {item.id: item for item in todo_dict.values() if item.owner == current_user.username}


@app.get("/todos/all")
async def get_all_todos(current_user: BaseUser = Depends(get_current_user)):
    if current_user.is_admin:
        return todo_dict


def validate_user_authentication(todo_id: int, current_user: BaseUser = Depends(get_current_user)):
    if todo_id not in todo_dict:
        raise ValueError("Not such todo.")
    if todo_dict[todo_id].owner != current_user.username and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# app.add_middleware(AuthMiddleware, verify_header=validate_user_authentication)


@app.get("/todos/{todo_id}")
async def get_specific_todo(todo_id: int, is_authenticated: bool = Depends(validate_user_authentication)):
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return todo_dict[todo_id]


@app.put("/todos/{todo_id}")
async def update_todo(todo_content: TodoContent, todo_id: int,
                      is_authenticated: bool = Depends(validate_user_authentication)):
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    todo_dict[todo_id] = Todo(**dict(todo_content), id=todo_id, owner=todo_dict[todo_id].owner)
    return todo_dict[todo_id]


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, is_authenticated: bool = Depends(validate_user_authentication)):
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return todo_dict.pop(todo_id)


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info")
