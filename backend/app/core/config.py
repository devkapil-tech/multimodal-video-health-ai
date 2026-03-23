from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Multimodal Video Health AI"
    data_dir: str = "data"
    frames_dir: str = "data/frames"
    outputs_dir: str = "data/outputs"
    frame_rate: int = 1  # frames per second to extract
    max_video_size_mb: int = 500
    llm_model: str = "llama3"         # swap with openai / mistral
    vision_model: str = "llava"       # swap with qwen-vl / gpt-4v
    whisper_model: str = "base"       # tiny / base / small / medium / large
    openai_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    database_url: str = ""
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"


settings = Settings()
