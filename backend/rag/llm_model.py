from ctransformers import AutoModelForCausalLM, AutoConfig

DEFAULT_MODEL_PATH = "./llm_models/llama-2-7b-chat.Q4_K_M/llama-2-7b-chat.Q4_K_M.gguf"

class LocalLLM:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH, max_new_tokens: int = 300, gpu_layers: int = 50):
        config = AutoConfig.from_pretrained(model_path)
        config.config.context_length = 1200
        config.config.max_new_tokens = max_new_tokens

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="llama",
            gpu_layers=gpu_layers,
            config=config
        )
        self.max_new_tokens = max_new_tokens

    def generate(self, prompt: str) -> str:
        """Generate response using the local LLM model."""
        resp = self.model(prompt, max_new_tokens=self.max_new_tokens)

        if isinstance(resp, str):
            return resp.strip()

        if isinstance(resp, list) and len(resp) > 0:
            return str(resp[0]).strip()

        return str(resp).strip()
