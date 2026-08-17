from services.ai.app.services.prompt_template import SYSTEM_PROMPT
from services.ai.app.schemas.ai_schemas import RetrivedChunks

class PromptBuilder:


    @staticmethod
    def build(question: str, chunks: list[RetrivedChunks]) -> str:

        if not chunks:
            context = "No relevent context found."
        else:
            context = "\n\n".join(
                f"[Chunk {index}]\n{chunk.get("content")}"
                for index, chunk in enumerate(chunks, start=1)
                )
        return f"""
{SYSTEM_PROMPT}

------------------------
Context
------------------------

{context}

------------------------
Question
------------------------

{question}

------------------------
Answer
------------------------
""".strip()