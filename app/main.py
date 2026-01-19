from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models, schemas, auth


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: schemas.Register, db: Session = Depends(get_db)):
    hashed = auth.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        password=hashed,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}

@app.post("/login")
def login(data: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=data.username).first()
    if not user or not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    otp_code = auth.generate_otp()
    otp = models.OTP(
        user_id=user.id,
        otp=otp_code,
        expires_at=auth.otp_expiry()
    )
    db.add(otp)
    db.commit()

    print("OTP:", otp_code)  # Console OTP

    return {"message": "OTP sent"}

@app.post("/verify-otp")
def verify(data: schemas.VerifyOTP, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=data.username).first()
    otp = db.query(models.OTP).filter_by(user_id=user.id, otp=data.otp, is_used=False).first()

    if not otp or otp.expires_at < auth.datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    otp.is_used = True
    user.is_verified = True
    db.commit()

    return {"message": "Login successful"}
