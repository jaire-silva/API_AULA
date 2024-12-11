from fastapi import APIRouter, HTTPException, Query
from firebase_admin import auth
import httpx
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")


router = APIRouter(
    prefix="/firebase",
    tags=["firebase"]
)


@router.get("/verify-token")
async def verify_token(id_token: str):
    try:
        # Verifica o token com o Firebase Auth
        decoded_token = auth.verify_id_token(id_token)
        return {"uid": decoded_token["uid"], "message": "Token válido"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.get("/login")
async def login(
    email: str = Query(..., description="Email do usuário para autenticação"),
    password: str = Query(..., description="Senha do usuário para autenticação")
):
    """
    Faz login no Firebase usando email e senha e retorna o id_token.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        # Faz a requisição POST para o Firebase Authentication usando httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response_data = response.json()

        # Log para depuração
        print(f"Resposta do Firebase: {response_data}")

        # Verifica se a resposta contém erro
        if response.status_code != 200:
            error_message = response_data.get("error", {}).get("message", "Erro desconhecido")
            raise HTTPException(status_code=response.status_code, detail=error_message)

        # Retorna o id_token
        return {
            "id_token": response_data["idToken"],
            "refresh_token": response_data["refreshToken"],
            "expires_in": response_data["expiresIn"]
        }

    except httpx.RequestError as e:
        # Erro ao realizar a requisição HTTP
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")

    except KeyError as e:
        # Erro se a resposta não contiver os campos esperados
        raise HTTPException(status_code=500, detail=f"Erro nos dados retornados: {str(e)}")

    except Exception as e:
        # Captura outros erros
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")