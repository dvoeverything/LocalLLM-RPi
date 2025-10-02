# LocalLLM-RPi: Run ChatGPT-style LLMs on Raspberry Pi 4B �

This project provides a comprehensive guide and tools for setting up and running small, ChatGPT-style language models locally on a Raspberry Pi 4B. It offers an end-to-end solution, covering installation, API usage, performance tuning, and troubleshooting, enabling you to harness the power of LLMs on resource-constrained hardware.

##  Key Features

- **Ollama Integration:** Seamlessly run LLMs using Ollama, a powerful tool for managing and deploying language models.
- **REST API Access:** Interact with the LLMs via a local REST API, enabling integration with other applications.
- **Python Examples:** Utilize provided Python scripts to easily interact with the API and build custom applications.
- **Hardware Optimization:** Get specific recommendations for hardware (Raspberry Pi 4B) and operating system (Raspberry Pi OS 64-bit) to maximize performance.
- **Performance Tuning:** Optimize your setup with tips on swap configuration, thermal management, and thread count adjustments.
- **Alternative llama.cpp Support:** Option to use `llama.cpp` for more control over GGUF quantized models.
- **Benchmark Results:** Review benchmark results for the Pi 4B (8GB) to understand expected performance.

## 🛠️ Tech Stack

| Category      | Technology                  | Description                                                                 |
|---------------|-----------------------------|-----------------------------------------------------------------------------|
| **LLM Runtime** | Ollama                      | Primary tool for running and managing LLMs.                               |
| **OS**          | Raspberry Pi OS 64-bit      | Recommended operating system for the Raspberry Pi 4B.                       |
| **API Client**  | Python `requests` library | Used in the example script for interacting with the REST API.                |
| **Alternative LLM Runtime** | llama.cpp                 | Alternative framework for running quantized models with fine-grained control. |
| **Hardware**    | Raspberry Pi 4B           | Target hardware platform.                                                   |

##  Getting Started

### Prerequisites

- Raspberry Pi 4B (recommended with 8GB RAM)
- Raspberry Pi OS 64-bit installed
- Internet connection for initial setup and model download

### Installation

1.  **Install Raspberry Pi OS 64-bit:** Follow the official Raspberry Pi documentation to install the 64-bit version of the OS on your Raspberry Pi.

2.  **Install Ollama:**
    ```bash
    curl -fsSL https://ollama.ai/install.sh | sh
    ```

3.  **Install Python `requests` library:**
    ```bash
    pip3 install requests
    ```

### Running Locally

1.  **Pull a Model:** Use Ollama to pull a pre-tuned model (e.g., TinyLlama, Llama 3.2, Qwen2.5):
    ```bash
    ollama pull tinyllama
    ```

2.  **Run the Model:** Start the model using Ollama:
    ```bash
    ollama run tinyllama "Write a short poem about Raspberry Pi."
    ```

3.  **Use the REST API (curl example):**
    ```bash
    curl -X POST http://localhost:11434/api/generate -d '{
      "model": "tinyllama",
      "prompt": "Write a short poem about Raspberry Pi."
    }'
    ```

4.  **Run the Python Example:** Navigate to the `examples` directory and run the `ollama_chat.py` script:
    ```bash
    cd examples
    python3 ollama_chat.py
    ```

## 💻 Usage

The primary way to interact with the LLMs is through the Ollama REST API. The `examples/ollama_chat.py` script provides a basic example of how to send messages to the API and stream the response.

**Example Python Usage:**

```python
import requests
import json

url = "http://localhost:11434/api/chat"

data = {
    "model": "tinyllama",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Write a short poem about Raspberry Pi."
        }
    ],
    "stream": False
}

response = requests.post(url, data=json.dumps(data), stream=False)

if response.status_code == 200:
    print(response.json()['message']['content'])
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## 📂 Project Structure

```
LocalLLM-RPi/
├── README.md
├── examples/
│   └── ollama_chat.py
```

## 📸 Screenshots

<img width="1917" height="1067" alt="Screenshot 2025-10-02 at 12 59 48 PM" src="https://github.com/user-attachments/assets/8e9597ba-1188-4021-8a27-196a9ddc4fb9" />
<img width="1336" height="843" alt="Screenshot 2025-10-02 at 1 01 26 PM" src="https://github.com/user-attachments/assets/f3021017-ef84-4956-8793-6fec68d6d75c" />


## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests with bug fixes, new features, or improvements to the documentation.

## 📝 License

This project is licensed under the [MIT License](LICENSE).


Thank you for checking out LocalLLM-RPi! We hope this project helps you explore the exciting world of local LLMs on your Raspberry Pi.


