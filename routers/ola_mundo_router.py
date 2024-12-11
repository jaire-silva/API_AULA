from fastapi import APIRouter

router = APIRouter(
    prefix="/ola-mundo",
    tags=["ola-mundo"]
)

@router.get("")
def ola_mundo():
    return {"Olá mundo!!!"}