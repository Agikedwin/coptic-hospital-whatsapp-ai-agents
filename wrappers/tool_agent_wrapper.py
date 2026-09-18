from memory.sharedState import AgentSharedState


def tool_node(state:AgentSharedState):


    query = state["messages"][-1].content


    result = tool_agent.invoke(
        {
          "query":query,
          "memory":state["memory"]
        }
    )


    return {

        "tool_results":result,

        "messages":[
          {
          "role":"assistant",
          "content":str(result)
          }
        ]
    }