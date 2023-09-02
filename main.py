import torch
from fastapi import FastAPI
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline

from data.prompt import prompt_template
from utils import CONFIG
from utils.gunicorn_logging import run_gunicorn_loguru

app = FastAPI()


@app.on_event("startup")
async def init_model():
    global pipe, generation_config
    logger.info(f"Loading model {CONFIG['model']['model_folder']}...")
    model = AutoModelForCausalLM.from_pretrained(
        "./models/" + CONFIG["model"]["model_folder"], torch_dtype=torch.float16, device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("./models/" + CONFIG["model"]["model_folder"])
    tokenizer.pad_token = tokenizer.eos_token
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=False,
    )
    generation_config = GenerationConfig(
        do_sample=True,
        max_new_tokens=32,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15,
        pad_token_id=tokenizer.eos_token_id,  # to rm warning
    )
    logger.info("Generation params:\n" + str(generation_config))


@app.get("/align")
async def align(task: str):
    prompt = prompt_template(task)
    logger.info(f"Received task: {task}")
    result = pipe(prompt, generation_config=generation_config)[0]['generated_text'].split("\n")[0]
    logger.info(f"SMART-aligned task: {result}")
    return {"smart-aligned-task": result}


if __name__ == '__main__':
    options = {
        "bind": CONFIG["app"]["host"] + ':' + CONFIG["app"]["port"],
        "workers": CONFIG["app"]["workers"],
        "timeout": CONFIG["app"]["timeout"],
    }
    run_gunicorn_loguru(app, options)
