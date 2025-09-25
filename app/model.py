# Created by Devesh Singh (Demonforms)
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from prompt import system_prompt
load_dotenv()

class Model(object):
    def __init__(self):
        self.index_name = "medical-chatbot-index"
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.model_name = "openai/gpt-oss-120b"
        self.embeddings = self.get_huggingface_embeddings()
        self.retriever = self.get_pinecone_retriever()
        self.chain = self.get_chain()

    def get_huggingface_embeddings(self):
        """Function to get huggingface embeddings this model is small and fast and output embeddings of size 384"""
        hf_embeddings = HuggingFaceEmbeddings(model_name = self.embedding_model)
        return hf_embeddings

    def get_pinecone_retriever(self):
        """Function to get the pinecone retriever from the existing index"""
        pc_index = PineconeVectorStore.from_existing_index(index_name=self.index_name, embedding=self.embeddings)
        retriever = pc_index.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        return retriever
    
    def get_chain(self):
        """Function to get the retrieval chain"""
        llm = ChatGroq(model = self.model_name, temperature = 0.5, max_tokens = 500)
        # create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}")
        ])

        # create the retrieval chain
        query_chain = create_stuff_documents_chain(llm = llm, prompt = prompt)
        chain = create_retrieval_chain(retriever = self.retriever, combine_docs_chain = query_chain)
        return chain
    
    def ask(self, query, context = list()):
        """Function to ask a query to the model"""
        # Build a prompt including previous messages
        prompt = ""
        for msg in context:
            role = msg["role"]
            content = msg["content"]
            prompt += f"{role}: {content}\n"
        
        # Add the new user query
        prompt += f"user: {query}\nassistant:"

        # Call the underlying chain with the full prompt
        response = self.chain.invoke({"input": prompt})
        
        return response["answer"]
    
# if __name__ == "__main__":
#     model = Model()
#     print(model.ask("What is Retrival Augmented Generation?"))