import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import list_files,create_folder,write_file,read_file,delete_file

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),".env"))
api_key=os.getenv("DEEPSEEK_API_KEY")
client=OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)
message=[
    {"role":"system","content":"你是我的文件管理助手。用户的文件都在 F:\\AI agent\\sandbox 文件夹里。所有操作都使用完整路径。"}
]
tool_functions= {
    "list_files":list_files,
    "create_folder":create_folder,
    "write_file":write_file,
    "read_file":read_file,
    "delete_file":delete_file,
}
tools=[
    {
        "type":"function",
        "function":{
            "name":"list_files",
            "description":"列出指定文件夹里的所有文件和文件夹，返回每行一个名字",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"文件夹的完整路径"
                    },
                },
                "required":["path"],
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"create_folder",
            "description":"在指定的路径中创造文件夹，若文件夹存在不报错",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"文件夹的完整路径"
                    },
                },
                "required":["path"],
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"write_file",
            "description":"在指定的文件路径中写入指定数据",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"文件夹的完整路径",
                    },
                    "content":{
                        "type":"string",
                        "description":"具体的内容",
                    },
                },
                "required":["path","content"],
            }
        }
    },
{
        "type":"function",
        "function":{
            "name":"read_file",
            "description":"阅读指定文件夹里的所有文件和文件夹",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"文件夹的完整路径"
                    },
                },
                "required":["path"],
            }
        }
    },
{
        "type":"function",
        "function":{
            "name":"delete_file",
            "description":"删除指定文件夹里的文件",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"文件夹的完整路径"
                    },
                },
                "required":["path"],
            }
        }
    },
]
print("AI大爷到! ! !")
print("输入quit结束对话")
while 1:
    question=input()
    if question=="quit":
        break
    else:
        message.append({"role":"user","content":question})
        while 1:
            response=client.chat.completions.create(
                model="deepseek-chat",
                messages=message,
                tools=tools
            )
            if response.choices[0].message.tool_calls:
                print("工具调用")
                message.append(response.choices[0].message)
                for tc in response.choices[0].message.tool_calls:
                    name=tc.function.name
                    args=json.loads(tc.function.arguments)
                    func=tool_functions[name]
                    result=func(**args)
                    message.append({
                        "role":"tool",
                        "tool_call_id":tc.id,
                        "content":str(result),
                    })
            else:
                print(response.choices[0].message.content)
                message.append({"role": "assistant", "content": response.choices[0].message.content})
                break