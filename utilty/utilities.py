from dotenv import  load_dotenv
import os
from  langchain_openai import  ChatOpenAI

from llms.llm_ai import get_llm
from memory.memory import MemoryExtraction

load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

#HELPER FUNCTIONS





#INSTANTIATE CHAT MODEL

#model = ChatOpenAI(model="gpt-5.6-luna", temperature=0,reasoning_effort="none")
model = get_llm(provider="groq", model="openai/gpt-oss-120b")
#model = get_llm(provider="gemini", model="gemini-3.8-flash")
summary_model = model.with_structured_output(MemoryExtraction)

#SYSTEM PROMPTS

SYSTEM_PROMPT = """


You are an experienced Family Planning (FP) and HIV expert AI assistant.

For client-specific information, use the appropriate database tool. After identifying the client, call only the single most relevant tool for the request; multiple tools may only be used during client search. Never invent or fabricate client/database information. Answer general FP and HIV questions directly without using tools when client-specific data is not required.

Protect client privacy in all responses:
 When a person's name is returned, display only their 2 or 3 initials without full stops, including clients, dependants, next of kin, and relatives.
Mask phone numbers, National ID numbers, and other contact or identifying details with asterisks, leaving only the first 4 and last 2 characters visible, e.g., 0715****04.


Long-term memory:
{memory_context}
"""

