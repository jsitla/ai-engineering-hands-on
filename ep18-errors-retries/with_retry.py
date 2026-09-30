"""
Episode 18 - the same request, with retries and a timeout.
The OpenAI library retries some errors for you (429, 5xx, connection errors),
waiting a little longer each time.
"""
import logging
import time

from openai import OpenAI

logging.basicConfig(format="%(asctime)s  %(message)s", datefmt="%H:%M:%S")
logging.getLogger("openai").setLevel(logging.INFO)  # show the retries

client = OpenAI(base_url="http://localhost:11500/v1", api_key="ollama",
                max_retries=4,   # try again up to 4 times
                timeout=30)      # give up on any single attempt after 30 seconds
start = time.perf_counter()
r = client.chat.completions.create(model="llama3.2:3b", messages=[{"role": "user", "content": "Say hi in three words."}])
print("answer:", r.choices[0].message.content)
print(f"took {time.perf_counter() - start:.1f} s in total")
