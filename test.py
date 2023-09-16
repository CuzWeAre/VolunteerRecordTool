from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

# 用户模型
class User(BaseModel):
    username: str
    password: str

# 用于模拟数据库的用户存储
users_db = {}

# OAuth2 配置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 用户注册
@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    users_db[user.username] = user.password
    return {"message": "Registration successful"}

# 用户登录并颁发令牌
@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(username=form_data.username, password=form_data.password)
    if user.username not in users_db or users_db[user.username] != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user.username, "token_type": "bearer"}

# 受保护的路由
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
