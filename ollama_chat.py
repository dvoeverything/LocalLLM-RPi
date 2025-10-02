
import requests, json

MODEL = "tinyllama:latest"  # or "llama3.2:1b" / "qwen2.5:1.5b"
URL = "http://localhost:11434/api/chat"

messages = [
    {"role": "system", "content": "You are Pi-IoT Assistant: concise, step-by-step."},
    {"role": "user", "content": "Give me a minimal example of using PWM on a Pi."}
]

resp = requests.post(URL, json={
    "model": MODEL,
    "messages": messages,
    "options": {"num_predict": 160, "temperature": 0.6}
}, stream=True)

for line in resp.iter_lines():
    if not line:
        continue
    data = json.loads(line.decode("utf-8"))
    chunk = data.get("message", {}).get("content", "")
    print(chunk, end="", flush=True)
