# LocalLLM-RPi
Run small, ChatGPT-style models fully on-device on a Raspberry Pi 4B (8 GB). This repo documents the end-to-end setup: install, run, API usage, tuning, and troubleshooting.

Table of Contents
Features
Hardware & OS
Quick Start (Ollama)
Use the Local REST API
Python Example (requests)
Alternative: llama.cpp
Performance Tips
Troubleshooting
Benchmarks (Pi 4B, 8 GB)
Project Structure
Roadmap
License
Features
One-command install with Ollama (CPU-only on Pi).
Pre-tuned commands for TinyLlama 1.1B, Llama 3.2 1B, Qwen2.5 1.5B.
Simple REST API to integrate with your apps.
Optional llama.cpp flow for maximum control over GGUF quantized models.
Pi-specific tuning (swap, thermal, threads) for smoother chats.
Hardware & OS
Raspberry Pi 4B (8 GB) (works on 4 GB with tighter limits).
Raspberry Pi OS 64-bit (very important).
Good cooling (heatsink + fan recommended).
Optional: external SSD (recommended if enabling larger swap).
Quick Start (Ollama)
Ollama is the easiest way to run small models locally.
# 1) Install Ollama (ARM64 build)
curl -fsSL https://ollama.com/install.sh | sh

# 2) Pull a small model
ollama pull tinyllama:latest
# Alternatives:
# ollama pull llama3.2:1b
# ollama pull qwen2.5:1.5b
# ollama pull qwen2.5-coder:1.5b

# 3) Chat interactively
ollama run tinyllama:latest
Tip: keep prompts short and set modest generation limits for snappy replies.
Use the Local REST API
Ollama exposes a local endpoint at http://localhost:11434.
Single completion (curl):
curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama:latest",
  "prompt": "Explain PWM on a Raspberry Pi in 3 bullets.",
  "options": {
    "num_predict": 120,
    "temperature": 0.7
  }
}'
Chat format (streaming):
curl -N http://localhost:11434/api/chat -d '{
  "model": "llama3.2:1b",
  "messages": [
    {"role":"system","content":"You are Pi-IoT Assistant: concise, step-by-step."},
    {"role":"user","content":"How do I read a DHT22 sensor on a Raspberry Pi?"}
  ]
}'
Python Example (requests)
# examples/ollama_chat.py
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
Run:
python3 examples/ollama_chat.py
Alternative: llama.cpp
If you want lower-level control, compile llama.cpp and run GGUF quantized weights.
# Build
sudo apt update
sudo apt install -y git build-essential cmake
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j4 LLAMA_NATIVE=1

# Place a quantized model in ./models (example filename shown)
# e.g., TinyLlama-1.1B-Chat.Q4_K_M.gguf
./main -m models/TinyLlama-1.1B-Chat.Q4_K_M.gguf \
  -t 3 -c 2048 -n 128 -ngl 0 \
  -p "You are Pi-IoT Assistant. Be concise. Q: How to enable I2C on Raspberry Pi?"
Flags:
-t 3 → threads (3 is often smoother on Pi 4).
-c 2048 → context length.
-n 128 → max tokens to generate.
-ngl 0 → CPU only (no GPU offload on Pi 4).
Performance Tips
Model size: stay ≤ 2B on Pi 4 for usable speeds.
Quantization: prefer Q4_K_M (good balance) or q4_0 to fit RAM.
Threads: start with -t 3 (or env OLLAMA_NUM_THREADS=3) to reduce throttling.
Context: 1024–2048 tokens is plenty for small models.
Swap (optional, SSD strongly recommended):
sudo sed -i 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
Thermals: use a fan/heatsink; consider the performance governor:
sudo apt install -y cpufrequtils
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl restart cpufrequtils
Troubleshooting
Very slow output (<1 tok/s)
Use a smaller model (TinyLlama 1.1B), reduce num_predict, lower -c, and set -t 3.
Out of memory / model won’t load
Use a more aggressive quant (Q4 instead of Q5), close other apps, increase swap (SSD).
Thermal throttling
Ensure active cooling; check with vcgencmd measure_temp and top/htop.
Ollama can’t bind port
Another process may be using 11434. Stop it or change the port: OLLAMA_HOST=0.0.0.0:11435 ollama serve.
Benchmarks (Pi 4B, 8 GB)
Your mileage will vary with cooling, OS, and flags.
Model (quant)	Context	Threads	Tokens/sec (est.)	Notes
TinyLlama 1.1B (Q4_K_M)	2048	3	~2–4	Best responsiveness
Llama 3.2 1B (Q4)	2048	3	~2–3	Newer tokenizer/instructions
Qwen2.5 1.5B (Q4)	1536	3	~1–2	Better reasoning, slower
Update this table with your actual runs (scripts/bench.sh if you add one).
Project Structure
.
├─ examples/
│  └─ ollama_chat.py        # Minimal Python streaming client
├─ README.md                # (this file)
└─ scripts/                 # (optional) helper scripts you add later
Roadmap
 Add systemd unit to run Ollama on boot.
 Add a tiny web UI (FastAPI/Flask) for chat in browser.
 Publish measured benchmarks per model/quant.
 Add Dockerfile (ARM64) for reproducible setup.
License
Choose a license for your repo (e.g., MIT). Remember, model weights you download have their own licenses—review them before redistribution.
