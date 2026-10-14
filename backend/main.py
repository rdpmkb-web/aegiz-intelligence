from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Aegiz Intelligence API",
    description="Motor Multi-Agente Autônomo - Startup em uma caixa",
    version="1.0.0"
)

# Configuração de CORS para permitir que o frontend converse com o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados recebido do Frontend
class BusinessInput(BaseModel):
    nome_negocio: str
    setor: str
    desafio_atual: str
    faturamento_estimado: Optional[float] = 50000.0

# Resposta estruturada dos Agentes
@app.post("/api/analisar")
def analisar_negocio(dados: BusinessInput):
    try:
        # Simulação do motor inteligente dos Agentes (Preparado para conectar à Groq/OpenAI)
        diagnostico = {
            "status": "Concluído",
            "nivel_maturidade": "Em validação inicial",
            "pontos_fortes": [
                f"Proposta clara para o setor de {dados.setor}",
                "Modelo de negócio escalável"
            ],
            "pontos_criticos": [
                f"Desafio crítico mapeado: {dados.desafio_atual}",
                "Necessidade de otimização no Custo de Aquisição (CAC)"
            ]
        }

        mercado = {
            "status": "Concluído",
            "oportunidades": [
                "Crescimento acelerado da demanda digital no segmento.",
                "Espaço para diferenciação através de transparência e autoridade."
            ],
            "hipoteses_vantagem": [
                "Hipótese 1: Parcerias estratégicas reduzem o CAC inicial em até 20%.",
                "Hipótese 2: Automatizar o atendimento aumenta a retenção em 15%."
            ]
        }

        execucao = {
            "status": "Concluído",
            "plano_30_dias": "Refinar a proposta de valor e estruturar os canais de captação inicial.",
            "plano_60_dias": "Lançar o MVP com campanhas segmentadas e recolher feedback.",
            "plano_90_dias": "Escalar tráfego pago e automatizar o funil de vendas e financeiro."
        }

        return {
            "sucesso": True,
            "negocio": dados.nome_negocio,
            "agente_diagnostico": diagnostico,
            "agente_mercado": mercado,
            "agente_execucao": execucao
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Aegiz Intelligence API está online e operando! 🚀"}

enzogogomes3
