import chromadb

client = chromadb.PersistentClient(path="./chromadb")

collection = client.get_or_create_collection(
    name="files"
)