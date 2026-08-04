from services.worker.app.chunking.recursive_chunker import RecursiveChunker


class ChunkerFactory:


    @staticmethod
    def get_chunker():
        return RecursiveChunker()