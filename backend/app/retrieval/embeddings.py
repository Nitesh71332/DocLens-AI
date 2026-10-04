from fastembed import TextEmbedding


model=TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def embed_texts(texts):
    return list(model.embed(texts))


def embed_query(query):
    return list(model.embed([query]))[0]