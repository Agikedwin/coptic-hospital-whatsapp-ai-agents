from dotenv import  load_dotenv
import os
from  langchain_openai import  ChatOpenAI

from memory.memory import MemoryExtraction

load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

#HELPER FUNCTIONS





#INSTANTIATE CHAT MODEL

model = ChatOpenAI(model="gpt-5.6-luna", temperature=0,reasoning_effort="none")
summary_model = model.with_structured_output(MemoryExtraction)

#SYSTEM PROMPTS

SYSTEM_PROMPT = """
You are a Family Planning expert Advisor and HIV expert experience AI assistant doctor. Provide accurate guidance on FP care, services, client history, and encounters.

Use tools for client-specific information. Always call a specific tool most relevant tool once the client has been search, no calling multiple tools except foe searching . Never fabricate database data. Answer general FP and HIV questions directly.

When results returned have patient name, hide full name and give only the 3 or 2 name initials without full stop(.) in between.


Long-term memory:
{memory_context}
"""

