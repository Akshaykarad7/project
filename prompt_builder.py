import os

def load_prompt_template(template_path: str) -> str:
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()

def build_prompt(generated_text: str, context: str, reference_data: str) -> str:
    template_path = os.path.join("prompts", "evaluation_prompt.txt")
    template = load_prompt_template(template_path)

    prompt = template.format(
        generated_text=generated_text.strip(),
        context=context.strip(),
        reference_data=reference_data.strip()
    )

    return prompt
