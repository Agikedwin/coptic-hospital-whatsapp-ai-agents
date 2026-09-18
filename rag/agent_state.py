from  langchain_core.documents import  Document
from langchain_core.prompts import ChatPromptTemplate

from rag.vectore_db import retriever
from typing import TypedDict, List
from  langchain_openai import  ChatOpenAI
from memory.memory import AgentState as SharedAgentState


from dotenv import  load_dotenv

load_dotenv()

#llm = ChatGroq(model="gpt-5.6-luna", temperature=0,reasoning_effort="none") # only for hosted models
llm = ChatOpenAI(model="gpt-5.6-luna", temperature=0,reasoning_effort="none")

class AgentState(TypedDict):
    question: str
    rewritten_question: str
    documents:  List[Document]
    generation: str
    relevance: str
    retry_count: int

#Query rewriter agent
def rewrite_query(state: AgentState):
    prompt =ChatPromptTemplate.from_template("""
    You are a query optimization agent.
    Rewrite the user question to improve retrieval from a knowledge base.
    Make it more specific and accurate and highly summarized.
    Do not add what the user has not asked for yet.
    
    Question: {question}
    
    """)

    chain = prompt | llm

    rewritten = chain.invoke(
        { "question": state["question"]}
    ).content
    print("\n++++++++++++++++++++++++++++++++++")
    print("Rewritten query: {}".format(rewritten))
    return {"rewritten_question": rewritten}


# Retrieval Agent
def retrieve(state: AgentState):
   query = state["rewritten_question"]
   docs = retriever.invoke(query)
   #Get only id and page content to save on token
   formatted_docs = [
       {
           "id": doc.id,
           "page_content": doc.page_content
       }
       for doc in docs
   ]

   return {
       "documents": formatted_docs
   }

# Relevance Agent
def grade_documents(state: AgentState):
   question = state["question"]
   docs = state["documents"]
   context = "\n\n".join(d['page_content']for d in docs)

   prompt = ChatPromptTemplate.from_template("""
      You are a strick relevance evaluator.
      Determine if the retrieved context is sufficient to answer the question .
      Make it more specific and accurate.

      Question: {question}
      
      Context: {context}
      
      Respond only with: relevant or not relevant
      """)

   chain = prompt | llm
   result = chain.invoke(
       {'question': question, 'context': context}
   ).content

   print("\n++++++++++++++++++++++++++++++++++")
   print("Relevance Result : ", result)
   return {"relevance": result}

#Answer generation
def generate(state: AgentState):
    context = "\n\n".join(d['page_content'] for d in state["documents"])
    prompt = ChatPromptTemplate.from_template(
        """
        You are a Family Planning AI expert.
        Answer the question using only the context below and give summarized response
        
        Context: {context}
        Question: {question}
        
        """
    )

    chain = prompt | llm
    answer = chain.invoke({
        "context": context,
        "question": state["question"]
    }).content

    return {"generation": answer}

#Decision Logic
def decide(state: AgentState):
    if state["relevance"] == "relevant":
        return "generate"
    if state["retry_count"] >=2:
        return "generate"
    return "generate"

#Retry tracker
def retry_tracker(state: AgentState):
    return {"retry_count": state["retry_count"] + 1}

def supervisor_node(
    state:SharedAgentState
):

    print("THE STATES ARE :")
    print(state)


    question = (
        state["messages"][-1:]
    )


    decision = llm.invoke(
        f"""
        
        Decide which agent should answer.
        
        Options:
        
        rag:
        - documents
        - policies
        - guidelines
        - knowledge
        
        tool:
        - database
        - API
        - actions
        
        both:
        - requires knowledge and action
        
        
        Question:
        
        {question}
        
        
        Return only:
        rag
        tool
        both
        
        """
            )


    return {
        "next_agent":
        decision.content.strip()

    }

