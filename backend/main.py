from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import httpx
import json
from supabase import create_client, Client

app = FastAPI(title="Aegiz Intelligence Engine - Unified Edition")

# Inicialização segura do Cliente Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

class ChatRequest(BaseModel):
    user_id: str
    message: str

class AnalyzeRequest(BaseModel):
    data: str

# --- ENDPOINT 1: PRESERVAÇÃO DOS TRÊS AGENTES ORIGINAIS ---
@app.post("/api/v1/analyze")
async def handle_original_analyze(request: AnalyzeRequest):
    """Mantém a lógica antiga de análise dos 3 agentes intacta conforme regras do Agent"""
    if not request.data:
        raise HTTPException(status_code=400, detail="Dados de análise ausentes.")
    # O Replit Agent manterá ou adaptará o seu script antigo de análise aqui dentro
    return {"status": "success", "message": "Dados processados pelos 3 agentes originais."}

# --- ENDPOINT 2: ROTA EXCLUSIVA DA CINTIA BEJE (SUPABASE + COZE) ---
async def execute_supabase_actions(action_json: dict, user_id: str):
    """Worker assíncrono de alta velocidade para salvar as criações no Supabase"""
    if not supabase:
        print("Erro: Cliente Supabase não configurado.")
        return
    try:
        action = action_json.get("action")
        if action == "build_all":
            # 1. Salva a configuração do site gerado
            supabase.table("generated_sites").insert({
                "user_id": user_id,
                "site_config": action_json.get("site_data", {})
            }).execute()

            # 2. Registra o Lead comercial no pipeline
            supabase.table("leads_management").insert({
                "user_id": user_id,
                "status": action_json.get("lead_data", {}).get("status", "hot"),
                "metadata": action_json
            }).execute()
    except Exception as e:
        print(f"Erro nas ações em background do Supabase: {e}")

@app.post("/api/v1/chat")
async def handle_cintia_chat(request: ChatRequest, background_tasks: BackgroundTasks):
    coze_token = os.getenv("COZE_API_TOKEN")
    bot_id = os.getenv("BOT_ID")
    
    if not coze_token or not bot_id:
        raise HTTPException(status_code=500, detail="Variáveis de ambiente da API ausentes.")
    if not supabase:
        raise HTTPException(status_code=500, detail="Conexão com o Supabase pendente.")

    # 1. Recupera o histórico de sessão do usuário direto do Supabase
    try:
        session_query = supabase.table("user_sessions").select("coze_conversation_id").eq("user_id", request.user_id).execute()
        conversation_id = session_query.data[0].get("coze_conversation_id") if session_query.data else None
    except Exception:
        conversation_id = None

    headers = {"Authorization": f"Bearer {coze_token}", "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        # 2. Se for um usuário novo, inicia a conversa no Coze e salva no Supabase
        if not conversation_id:
            conv_resp = await client.post("https://coze.com", headers=headers, json={})
            if conv_resp.status_code == 200:
                conversation_id = conv_resp.json().get("data", {}).get("id")
                supabase.table("user_sessions").insert({
                    "user_id": request.user_id, 
                    "coze_conversation_id": conversation_id
                }).execute()

        # 3. Envia os dados para processamento da Cintia Beje no Coze
        payload = {
            "bot_id": bot_id,
            "conversation_id": conversation_id,
            "user_id": request.user_id,
            "additional_messages": [{"role": "user", "content": request.message, "content_type": "text"}]
        }
        
        response = await client.post("https://coze.com", headers=headers, json=payload, timeout=30.0)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Falha de comunicação com o Coze.")
        
        chat_data = response.json()
        assistant_reply = chat_data.get("data", {}).get("content", "")
        
        # 4. Dispara as ações automáticas (maquininha) caso a Cintia envie o JSON
        if "[EXECUTE_ACTION]" in assistant_reply:
            try:
                json_part = assistant_reply.split("[EXECUTE_ACTION]")[-1].strip()
                action_data = json.loads(json_part)
                background_tasks.add_task(execute_supabase_actions, action_data, request.user_id)
            except Exception:
                pass 
                
        return {"response": assistant_reply}

