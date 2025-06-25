from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import generate_response, classify_intent
from backend.calendar_utils import create_event
from dateutil import parser
from datetime import datetime
from typing import Optional

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input and output schemas
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    event_link: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message
    intent = classify_intent(user_message)

    if intent == "book":
        try:
            # Parse datetime from message
            dt = parser.parse(user_message, fuzzy=True)
            event_link = create_event("Appointment", dt)

            return ChatResponse(
                response=f" Appointment booked for {dt.strftime('%A %d %B %Y at %I:%M %p')}.",
                event_link=event_link
            )
        except Exception as e:
            return ChatResponse(
                response=" Sorry, I couldn't understand the appointment time. Could you rephrase it?"
            )

    # Else use LLM for general response
    reply = generate_response(user_message)
    return ChatResponse(response=reply)
