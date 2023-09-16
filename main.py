from fastapi import FastAPI, HTTPException, Depends
from manage_sql import ManageSql
from pydantic import BaseModel
from user_auth import UserAuth
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

sql = ManageSql()
app = FastAPI()


class User(BaseModel):
    student_id: str
    password: str
    username: str


class Activity(BaseModel):
    activity_id: str
    activity_name: str
    volunteer_hours: float
    activity_info: str


# OAuth2 配置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/admin/shutdown")
async def shutdown():
    sql.close()
    return {"message": "SQL connection has been closed"}


@app.post("/register/")
async def register(user: User):
    # 检查用户名是否已经存在
    if sql.query(value_to_check=user.student_id)[0]:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password, salt = UserAuth.hashpw(user.password)
    register_data = (user.student_id, hashed_password, salt, user.username)
    # 存储用户信息
    sql.register(register_data)

    return {"message": f"User {user.student_id} registered successfully"}


@app.post("/activity_add/")
async def register(activity: Activity):
    # 检查活动是否已经存在
    if sql.query(table="activities", key="activity_id", value_to_check=activity.activity_id)[0]:
        raise HTTPException(status_code=400, detail="Activity already exists")
    activity_data = (activity.activity_id, activity.activity_name, activity.volunteer_hours, activity.activity_info)
    # 存储活动信息
    sql.activity_add(activity_data)

    return {"message": f"Activity {activity.activity_id} added successfully"}


# 用户登录并颁发令牌
@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(student_id=form_data.username, password=form_data.password)
    user_data = sql.query(value_to_check=user.username)
    if not user_data[0] and not UserAuth.auth(user.password, user_data[1][2], user_data[1][1]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user.username, "token_type": "bearer"}


# 受保护的路由
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
