import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"


def consultar_groq(mensagem: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY não configurada.")

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "user",
                "content": mensagem
            }
        ],
        "max_completion_tokens": 300
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        resultado = response.json()

        return resultado["choices"][0]["message"]["content"]

    except requests.RequestException as exc:
        raise RuntimeError(
            "Não foi possível consultar o serviço de IA."
        ) from exc
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise RuntimeError(
            "A resposta recebida da IA não tem o formato esperado."
        ) from exc
