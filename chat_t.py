from openai import AsyncOpenAI
import httpx
import utils

client = AsyncOpenAI(
            api_key = 1,
            base_url = "https://api.deepseek.com",
            http_client=httpx.AsyncClient(proxy=proxy_url)
            )


msglist = []

async def get_response(client, model, tempreture, msglist):
    full_response = ""
    try:
        stream = await client.chat.completions.create(
                model = model,
                messages = msglist,
                stream = True,
                tempreture = tempreture,
                reasonin_effort = "max",
                extra_body = {"thinking": {"type": "enabled"}}
                )

        async for chunk in stream:
            delta =  chunk.choices[0].delta.content
            if delta:
                full_response += delta

    except Exception as e:
        error_msg = f"Error: {str(e)}"

    return full_response



