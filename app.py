import gradio as gr
from utils.reference_loader import get_reference_data
from model.model_loader import LLMWrapper
from utils.prompt_builder import build_prompt
import json

def format_output(output_text):
    """Convert the raw JSON-like string into clean markdown."""
    try:
        output_json = json.loads(output_text)
        final_output = f"### 🧾 Composite Score: {output_json.get('composite_score', 'N/A')}\n"

        eval_data = output_json.get("evaluation", {})
        for aspect, details in eval_data.items():
            final_output += f"\n**{aspect.capitalize()}**\n- Score: {details.get('score', 'N/A')}\n- Comments: {details.get('comments', '')}\n"

        suggestions = output_json.get("suggestions", {})
        if suggestions:
            final_output += "\n### ✏️ Suggestions\n"
            final_output += f"**Revised Text**\n> {suggestions.get('revise', '')}\n\n"
            final_output += f"**Additions**\n> {suggestions.get('additions', '')}\n"

        return final_output
    except Exception:
        return output_text  # fallback if it's not JSON

def evaluate_interface(input_type, reference_input, pdf_file, wiki_topic,url_input, user_query, generated_text, context):
    if input_type == "text":
        input_value = reference_input
    elif input_type == "pdf":
        input_value = pdf_file.name if pdf_file else ""
    elif input_type == "wiki":
        input_value = wiki_topic
    elif input_type=="url":
        input_value=url_input

    else:
        return "❌ Invalid input type.", ""

    try:
        reference_data = get_reference_data(input_type=input_type, input_value=input_value, query=user_query)
        prompt = build_prompt(generated_text, context, reference_data)
        model = LLMWrapper()
        output = model.generate(prompt)
        return "✅ Evaluation successful.", format_output(output)
    except Exception as e:
        return "❌ Error", str(e)

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Automated Text Evaluation Tool")

    with gr.Column():
        input_type = gr.Radio(["text", "pdf", "wiki","url"], label="1️⃣ Select Reference Type", value="text")

        reference_input = gr.Textbox(label="📄 Paste Reference Text", visible=True)
        pdf_file = gr.File(label="📁 Upload PDF", file_types=[".pdf"], visible=False)
        wiki_topic = gr.Textbox(label="🌐 Wikipedia Topic", visible=False)
        url_input = gr.Textbox(label="🔗 Website URL", visible=False)

        def toggle_inputs(choice):
            return {
                reference_input: gr.update(visible=choice == "text"),
                pdf_file: gr.update(visible=choice == "pdf"),
                wiki_topic: gr.update(visible=choice == "wiki"),
                url_input: gr.update(visible=choice == "url")
            }

        input_type.change(toggle_inputs, input_type, [reference_input, pdf_file, wiki_topic,url_input])

        user_query = gr.Textbox(label="🔍 User Query", placeholder="E.g. Is this factually correct?")
        generated_text = gr.Textbox(label="📝 Generated Text", lines=6, placeholder="Paste the generated text here.")
        context = gr.Textbox(label="📚 Context", placeholder="E.g. Essay for school, blog post for young adults, etc.")

        submit_btn = gr.Button("🚀 Run Evaluation")
        status = gr.Textbox(label="Status", interactive=False)
        output = gr.Markdown(label="📋 Evaluation Output")

        submit_btn.click(
            evaluate_interface,
            inputs=[input_type, reference_input, pdf_file, wiki_topic,url_input, user_query, generated_text, context],
            outputs=[status, output]
        )

demo.launch()

