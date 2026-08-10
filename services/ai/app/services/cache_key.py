import hashlib

class CacheKet:

    PREFIX = "ai:answer"

    @classmethod
    def generate(cls, question: str) -> str:
        normalized_question = question.strip().lower()

        question_hash = hashlib.sha3_256(
            normalized_question.encode("utf-8")
        ).hexdigest()

        return f"{cls.PREFIX}:{question_hash}"