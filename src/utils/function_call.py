import json
from typing import Tuple, Union

from ..type import ChatMessage, DeltaMessage, FunctionCallResponse

OBSERVATION = "Observation"

TOOL_DESC = """{name}: Call this tool to interact with the {name} API. \
What is the {name} API useful for? \
{description} \
Parameters: {parameters}. Format the arguments as a JSON object."""


# Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.
REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
{OBSERVATION}: the result of the action
... (this Thought/Action/Action Input/{OBSERVATION} can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {query}"""

def need_function_call(messages, functions):
    if functions is not None and len(functions) > 0:
        return True
    if messages is not None and len(messages) > 0 and messages[-1].role == "function":
        return True
    return False

def build_function_call_message(messages, functions, function_call="auto"):
    if messages is None or len(messages) == 0:
        return None
    if functions is None or function_call == 'none':
        return messages[-1]
    if function_call != "auto" and isinstance(function_call, dict):
        functions = [f for f in functions if f.name in [function_call.name]]

    tool_descs, tool_names = [], []
    for f in functions:
        tool_descs.append( TOOL_DESC.format( name=f.name, description=f.description, parameters=json.dumps(f.parameters, ensure_ascii=False)))
        tool_names.append(f.name)
    tool_descs = "\n\n".join(tool_descs)
    tool_names = ", ".join(tool_names)

    
    last = ""
    for message in messages[-1::-1]:
        if message.role == "user":
            last += REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names, query=message.content, OBSERVATION=OBSERVATION)
            break
        elif message.role == "assistant":
            if message.function_call:
                function_name = message.function_call.name
                arguments = message.function_call.arguments
                last += f"\nThought: I should call {function_name} with {arguments}"
                last += f"\nAction: {function_name.strip()}"
                last += f"\nAction Input: {arguments.strip()}"
        elif message.role == "function":
            last += f"\n{OBSERVATION}: output of {message.name} is {str(message.content).strip()}"

    return ChatMessage(role="user", content=last)


def build_chat_message(response: str) -> ChatMessage:
    parsed = _parse_qwen_plugin_call(response)
    if parsed is None:
        return ChatMessage(role="assistant", content=response), "stop"
    else:
        name, args, final = parsed
        if final:
            return ChatMessage(role="assistant", content=final), "stop"
        else:
            function_call = FunctionCallResponse(name=name, arguments=args)
            return ChatMessage(role="assistant", content=None, function_call=function_call), "function_call"

def build_fc_name_message(text: str) -> DeltaMessage:
    i = text.rfind('\nAction:')
    j = text.rfind('\nAction Input:')
    name = text[i + len('\nAction:'): j].strip()
    return DeltaMessage(function_call=FunctionCallResponse(name=name, arguments=""))

def build_fc_args_message(delta: str) -> DeltaMessage:
    return DeltaMessage(function_call=FunctionCallResponse(arguments=delta))

def _parse_qwen_plugin_call(text: str) -> Union[Tuple[str, str], None]:
    i = text.rfind('\nAction:')
    j = text.rfind('\nAction Input:')
    k = text.rfind('\nObservation:')
    l = text.rfind('\nFinal Answer:')

    if l >= 0:
        final = text[l + len('\nFinal Answer:'):].strip()
        return None, None, final

    if 0 <= i < j:  # If the text has `Action` and `Action input`,
        if k < j:  # but does not contain `Observation`,
            # then it is likely that `Observation` is ommited by the LLM,
            # because the output text may have discarded the stop word.
            text = text.rstrip() + '\nObservation:'  # Add it back.
            k = text.rfind('\nObservation:')

    if 0 <= i < j < k:
        name = text[i + len('\nAction:'): j].strip()
        args = text[j + len('\nAction Input:'): k].strip()
        return name, args, None
    return None