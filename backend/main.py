from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Aegiz Intelligence API",
    description="Motor Multi-Agente Autônomo - Startup em uma caixa",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BusinessInput(BaseModel):
    nome_negocio: str
    setor: str
    desafio_atual: str
    faturamento_estimado: Optional[float] = 50000.0


@app.post("/api/analisar")
def analisar_negocio(dados: BusinessInput):
    try:
        diagnostico = {
            "status": "Concluído",
            "nivel_maturidade": "Em validação inicial",
            "pontos_fortes": [
                f"Proposta clara para o setor de {dados.setor}",
                "Modelo de negócio escalável",
            ],
            "pontos_criticos": [
                f"Desafio crítico mapeado: {dados.desafio_atual}",
                "Necessidade de otimização no Custo de Aquisição (CAC)",
            ],
        }

        mercado = {
            "status": "Concluído",
            "oportunidades": [
                "Crescimento acelerado da demanda digital no segmento.",
                "Espaço para diferenciação através de transparência e autoridade.",
            ],
            "hipoteses_vantagem": [
                "Hipótese: parcerias estratégicas podem reduzir o CAC inicial.",
                "Hipótese: automatizar o atendimento pode aumentar a retenção.",
            ],
        }

        execucao = {
            "status": "Concluído",
            "plano_30_dias": (
                "Refinar a proposta de valor e estruturar os canais "
                "de captação inicial."
            ),
            "plano_60_dias": (
                "Lançar o MVP com campanhas segmentadas e recolher feedback."
            ),
            "plano_90_dias": (
                "Avaliar canais de aquisição e otimizar o funil de vendas."
            ),
        }

        return {
            "sucesso": True,
            "negocio": dados.nome_negocio,
            "agente_diagnostico": diagnostico,
            "agente_mercado": mercado,
            "agente_execucao": execucao,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível analisar os dados do negócio.",
        ) from None


@app.get("/")
def root():
    return {"message": "Aegiz Intelligence API está online!"}
