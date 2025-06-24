# core/session_storage.py

user_sessions = {}

def get_user_session(user_id):
    user_id = str(user_id)  # Cast to str for consistency
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "text": None,
            "image_path": None,
            "memory": []
        }
    return user_sessions[user_id]

def store_user_input(user_id, key, value):
    session = get_user_session(str(user_id))  # Use str here too
    session[key] = value

def append_to_memory(user_id, user_msg, bot_reply):
    session = get_user_session(str(user_id))
    session["memory"].append((user_msg, bot_reply))
    session["memory"] = session["memory"][-5:]

def get_user_memory(user_id):
    return get_user_session(str(user_id))["memory"]

def clear_user_session(user_id):
    user_sessions[str(user_id)] = {
        "text": None,
        "image_path": None,
        "memory": []
    }
