class ChatHistory:
    def __init__(self):
        self.history = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.history:
            self.history[session_id] = []
        self.history[session_id].append({"role": role, "content": content})

    def get_history(self, session_id):
        return self.history.get(session_id, [])

    def clear_history(self, session_id):
        if session_id in self.history:
            del self.history[session_id]

chat_history = ChatHistory()