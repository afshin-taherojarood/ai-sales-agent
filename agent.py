from openai import OpenAI
import os
import json
from prompts import SALES_AGENT_PROMPT
from tools import check_price, check_inventory, get_specs, list_products, register_order



class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "check_price",
                    "description": "چک کردن قیمت محصول",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "نام محصول مثل ایسوس، لنوو، اچ پی"
                            }
                        },
                        "required": ["product_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_inventory",
                    "description": "چک کردن موجودی محصول",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "نام محصول"
                            }
                        },
                        "required": ["product_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_specs",
                    "description": "گرفتن مشخصات محصول",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "نام محصول"
                            }
                        },
                        "required": ["product_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_products",
                    "description": "نمایش لیست همه محصولات موجود",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "register_order",
                    "description": "ثبت سفارش مشتری بعد از گرفتن اطلاعات کامل",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_name": {
                                "type": "string",
                                "description": "نام مشتری"
                            },
                            "phone": {
                                "type": "string",
                                "description": "شماره تماس مشتری"
                            },
                            "address": {
                                "type": "string",
                                "description": "آدرس مشتری"
                            },
                            "product_name": {
                                "type": "string",
                                "description": "نام محصول"
                            }
                        },
                        "required": ["customer_name", "phone", "address", "product_name"]
                    }
                }
            }
        ]

        self.messages = [
            {
                "role": "system",
                "content": SALES_AGENT_PROMPT
            }
        ]

    def run_tool(self, tool_name, tool_args):
        print(f"🔧 Tool: {tool_name}, Args: {tool_args}")
        if tool_name == "check_price":
            return check_price(tool_args["product_name"])
        elif tool_name == "check_inventory":
            return check_inventory(tool_args["product_name"])
        elif tool_name == "get_specs":
            return get_specs(tool_args["product_name"])
        elif tool_name == "list_products":
            return list_products()
        elif tool_name == "register_order":
            return register_order(
                tool_args["customer_name"],
                tool_args["phone"],
                tool_args["address"],
                tool_args["product_name"]
            )

    def chat(self, user_input):
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        response = self.client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=self.messages,
            tools=self.tools
        )

        # حلقه برای handle کردن چند tool call
        while response.choices[0].finish_reason == "tool_calls":
            tool_calls = response.choices[0].message.tool_calls

            self.messages.append(response.choices[0].message)

            # اجرای همه tool calls
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_result = self.run_tool(tool_name, tool_args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })

            response = self.client.chat.completions.create(
                model="google/gemini-2.0-flash-001",
                messages=self.messages,
                tools=self.tools
            )

        assistant_message = response.choices[0].message.content

        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message