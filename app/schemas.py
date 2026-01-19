from pydantic import BaseModel

class Register(BaseModel):
    username: str
    password: str
    email: str

class Login(BaseModel):
    username: str
    password: str

class VerifyOTP(BaseModel):
    username: str
    otp: str
