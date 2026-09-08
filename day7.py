documents = [
    "Python is a programming language.",
    "NumPy is used for numerical computing.",
    "Pandas is used for data analysis.",
    "Matplotlib is used for data visualization."
]


def retrieve(query):

    query = query.lower()

    for document in documents:
        if "numpy" in query and "numpy" in document.lower():
            return document

        if "pandas" in query and "pandas" in document.lower():
            return document

        if "matplotlib" in query and "matplotlib" in document.lower():
            return document

    return "No relevant information found."


def rag(question):

    context = retrieve(question)

    answer = f"""
Based on the retrieved information:

{context}

Answer generated using the retrieved context.
"""

    return answer


question = input("Ask: ")

print(rag(question))