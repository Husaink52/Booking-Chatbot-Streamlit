from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import ConversationChain

# Load Hugging Face model (you can replace with any compatible model)
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=100,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.2
)

llm = HuggingFacePipeline(pipeline=pipe)
conversation = ConversationChain(llm=llm)

# LLM Response Generator
def generate_response(message: str) -> str:
    return conversation.run(message)

# Rule-based Intent Classifier
def classify_intent(message: str) -> str:
    message_lower = message.lower()
    keywords = ["book", "appointment", "schedule", "meeting", "reserve"]
    for keyword in keywords:
        if keyword in message_lower:
            return "book"
    return "chat"
