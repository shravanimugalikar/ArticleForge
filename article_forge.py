import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import os
from dotenv import load_dotenv
import gradio as gr
import crewai.llms.cache

# Fix CrewAI prompt caching compatibility with Groq
crewai.llms.cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Agent, Task, Crew, LLM

load_dotenv()


DEFAULT_MODEL = "groq/openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 0.7


def generate_article(topic: str, progress=gr.Progress()):
    if not topic or not topic.strip():
        return "⚠️ Please enter a topic to generate an article."

    progress(0.1, desc="Initializing Groq LLM & CrewAI agents...")

    llm = LLM(
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE
    )

    planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article "
                  "about the topic: {topic}. "
                  "You collect information that helps the audience learn something "
                  "and make informed decisions. Your work is the basis for the Content Writer.",
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate "
             "opinion piece about the topic: {topic}",
        backstory="You're working on writing a new opinion piece about the topic: {topic}. "
                  "You base your writing on the work of the Content Planner, who provides an outline "
                  "and relevant context about the topic. You follow the main objectives and "
                  "direction of the outline, providing objective and impartial insights.",
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with the writing style of the organization.",
        backstory="You are an editor who receives a blog post from the Content Writer. "
                  "Your goal is to review the blog post to ensure that it follows journalistic best practices, "
                  "provides balanced viewpoints when providing opinions or assertions, "
                  "and avoids major controversial topics or opinions when possible.",
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering their interests and pain points.\n"
            "3. Develop a concise content outline including an introduction, key sections, and a call to action.\n"
            "4. Include target SEO keywords."
        ),
        expected_output="A concise content plan outline (under 350 words) with key sections and SEO keywords.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use the content plan to craft a compelling, well-structured blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Ensure the post is structured with an engaging introduction, insightful body sections, and a summarizing conclusion.\n"
            "4. Keep the draft focused and concise (around 500-700 words, 2-3 paragraphs per main section).\n"
        ),
        expected_output="A well-written blog post in markdown format (around 500-700 words) ready for publication.",
        agent=writer,
        context=[plan],
    )

    edit = Task(
        description="Proofread the written blog post. Correct any grammatical errors, refine readability, and align with a professional voice. Output the complete edited blog post.",
        expected_output="The polished, publication-ready blog post in clean markdown format (around 500-700 words).",
        agent=editor,
        context=[write],
    )

    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=True
    )

    progress(0.3, desc="Content Planner, Writer & Editor agents are working...")
    try:
        result = crew.kickoff(inputs={"topic": topic.strip()})
        progress(1.0, desc="Article successfully generated!")
        return str(result)
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower() or "tpm" in error_msg.lower():
            return (
                "⚠️ **Groq Rate Limit Reached**\n\n"
                "The request exceeded Groq's Tokens Per Minute (TPM) limit on the free tier.\n\n"
                "**What to do:** Please wait 30–60 seconds for the quota to reset, then click **Generate Article** again."
            )
        return f"⚠️ **An error occurred during generation:**\n\n{error_msg}"


def build_app():
    with gr.Blocks(title="ArticleForge") as demo:
        gr.Markdown("# ✍️ ArticleForge")
        gr.Markdown(
            "An autonomous multi-agent team (**Content Planner** ➔ **Content Writer** ➔ **Editor**) "
            "powered by **CrewAI** and **Groq**."
        )

        with gr.Row():
            with gr.Column(scale=1):
                topic_input = gr.Textbox(
                    label="Article Topic",
                    placeholder="e.g. Artificial Intelligence, Quantum Computing, Autonomous Driving...",
                    lines=3
                )
                submit_btn = gr.Button("🚀 Generate Article", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear")

                gr.Examples(
                    examples=[
                        ["Artificial Intelligence in Healthcare"],
                        ["The Future of Quantum Computing"],
                        ["Autonomous Electric Vehicles in 2026"],
                        ["Agentic AI and the Modern Digital Labor Force"]
                    ],
                    inputs=topic_input
                )

            with gr.Column(scale=2):
                output_markdown = gr.Markdown(
                    label="Generated Article",
                    value="*Your generated article will appear here...*"
                )

        submit_btn.click(
            fn=generate_article,
            inputs=[topic_input],
            outputs=output_markdown
        )
        clear_btn.click(
            fn=lambda: ("", "*Your generated article will appear here...*"),
            outputs=[topic_input, output_markdown]
        )

    return demo


if __name__ == "__main__":
    demo = build_app()
    demo.launch(theme=gr.themes.Soft(), inbrowser=True)