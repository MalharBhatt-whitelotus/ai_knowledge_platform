import json
import hashlib

class CacheKey:

    PREFIX = "ai:answer"

    @classmethod
    def generate(cls, chunks: list[str], question: str) -> str:
        payload = {
            "question": question.strip().lower(),
            "chunks": [chunk.get("content") for chunk in chunks],
        }

        raw = json.dumps(payload, sort_keys=True)

        digest = hashlib.sha3_256(
            raw.encode("utf-8")
        ).hexdigest()

        return f"{cls.PREFIX}:{digest}"