import json
from datetime import datetime
from supabase import create_client, Client
import random

# --- БАПТАУЛАР ---
# Сіздің жобаңыздың URL мекенжайы (автоматты түрде қойдым)
SUPABASE_URL = "https://kgdhjkuaufsinbyaltin.supabase.co"

# ⚠️ ОСЫ ЖЕРГЕ КІЛТТІ ҚОЙЫҢЫЗ (Settings -> API -> anon key)
SUPABASE_KEY = "sb_publishable_ocFzfPWfI6pGgFJvV8Fchw_13v5T7sM"

# Клиентті іске қосу
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase қосылу қатесі: {e}")

# Сұрақтарды импорттау
try:
    from questions import ALL_DATA
except ImportError:
    ALL_DATA = {}

def init_db():
    """Базаны тексереді және сұрақтар жоқ болса, жүктейді."""
    try:
        # Сұрақтар бар ма тексереміз
        response = supabase.table('questions').select("id", count="exact").execute()
        count = response.count
        
        if count == 0 and ALL_DATA:
            print("База бос, сұрақтар жүктелуде...")
            mapping = {
                "history": "Қазақстан тарихы",
                "math": "Математикалық сауаттылық",
                "reading": "Оқу сауаттылығы"
            }
            
            bulk_data = []
            for key, qs in ALL_DATA.items():
                subject_name = mapping.get(key, key)
                for q in qs:
                    expl = q.get('explanation', 'Түсіндірме жоқ.')
                    bulk_data.append({
                        "subject": subject_name,
                        "question": q['q'],
                        "options": json.dumps(q['opts']),
                        "answer": q['a'],
                        "explanation": expl
                    })
            
            # 100 сұрақтан бөліп салу (API шектеуіне байланысты)
            chunk_size = 100
            for i in range(0, len(bulk_data), chunk_size):
                supabase.table('questions').insert(bulk_data[i:i+chunk_size]).execute()
            print("Сұрақтар сәтті жүктелді!")
            
    except Exception as e:
        print(f"init_db қатесі: {e}")

# --- ҚОЛДАНУШЫЛАР ---
def login_user(username, password):
    try:
        response = supabase.table('users').select("*").eq('username', username).eq('password', password).execute()
        if response.data:
            return response.data[0]
    except: pass
    return None

def register_user(username, full_name, password):
    try:
        check = supabase.table('users').select("id").eq('username', username).execute()
        if check.data:
            return False
        
        supabase.table('users').insert({
            "username": username,
            "full_name": full_name,
            "password": password
        }).execute()
        return True
    except: return False

def change_password(user_id, new_password):
    try:
        supabase.table('users').update({"password": new_password}).eq('id', user_id).execute()
        return True
    except: return False

# --- ТЕСТ ЖӘНЕ НӘТИЖЕЛЕР ---
def save_result(user_id, subject, score, total):
    try:
        supabase.table('results').insert({
            "user_id": user_id,
            "subject": subject,
            "score": score,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }).execute()
    except Exception as e: print(f"Қате: {e}")

def get_questions_by_subject(subject, limit=10):
    try:
        response = supabase.table('questions').select("*").eq('subject', subject).execute()
        data = response.data
        if not data: return []
        
        random.shuffle(data)
        selected = data[:limit]
        
        return [{
            "id": r["id"],
            "q": r["question"],
            "opts": json.loads(r["options"]),
            "a": r["answer"],
            "expl": r["explanation"]
        } for r in selected]
    except Exception as e:
        print(f"Сұрақ алу қатесі: {e}")
        return []

def get_my_results(user_id):
    try:
        response = supabase.table('results').select("*").eq('user_id', user_id).order('id', desc=True).execute()
        return response.data
    except: return []

def get_leaderboard_general():
    try:
        response = supabase.table('leaderboard_view').select("*").execute()
        return response.data
    except: return []

def get_user_stats(user_id):
    try:
        res_count = supabase.table('results').select("id", count="exact").eq('user_id', user_id).execute()
        total_tests = res_count.count
        
        res_scores = supabase.table('results').select("score, total").eq('user_id', user_id).execute()
        if not res_scores.data:
            return 0, 0
            
        percentages = [(r['score'] / r['total'] * 100) for r in res_scores.data if r['total'] > 0]
        avg_score = sum(percentages) / len(percentages) if percentages else 0
        
        return total_tests, avg_score
    except: return 0, 0

# --- МҰҒАЛІМ ФУНКЦИЯЛАРЫ ---
def get_all_questions_for_teacher():
    try:
        response = supabase.table('questions').select("id, subject, question").order('id', desc=True).execute()
        return response.data
    except: return []

def delete_question(question_id):
    try:
        supabase.table('questions').delete().eq('id', question_id).execute()
        return True
    except: return False

def add_question(subject, question, opts, answer, explanation=""):
    try:
        supabase.table('questions').insert({
            "subject": subject,
            "question": question,
            "options": json.dumps(opts),
            "answer": answer,
            "explanation": explanation
        }).execute()
        return True
    except: return False

# --- САҚТАЛҒАН СҰРАҚТАР ---
def toggle_save_question(user_id, question_id):
    try:
        check = supabase.table('saved_questions').select("id").eq('user_id', user_id).eq('question_id', question_id).execute()
        if check.data:
            supabase.table('saved_questions').delete().eq('user_id', user_id).eq('question_id', question_id).execute()
            return False
        else:
            supabase.table('saved_questions').insert({"user_id": user_id, "question_id": question_id}).execute()
            return True
    except: return False

def is_question_saved(user_id, question_id):
    try:
        check = supabase.table('saved_questions').select("id").eq('user_id', user_id).eq('question_id', question_id).execute()
        return len(check.data) > 0
    except: return False

def get_saved_questions(user_id):
    try:
        response = supabase.table('saved_questions').select("question_id, questions(id, subject, question, answer, explanation)").eq('user_id', user_id).execute()
        formatted = []
        for item in response.data:
            q = item['questions']
            if q:
                formatted.append({
                    "id": q['id'],
                    "subject": q['subject'],
                    "question": q['question'],
                    "answer": q['answer'],
                    "explanation": q['explanation']
                })
        return formatted
    except: return []
