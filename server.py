from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv('GROQ_API_KEY')
model=ChatGroq(model='gemma2-9b-it',groq_api_key=groq_api_key)


# 1. create a prompy=t template
###prompt templates
from langchain_core.prompts import ChatPromptTemplate
system_template="translate in to {languages}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),('user',"{text}")
 ]
)
parser =StrOutputParser()


#create chain
chain=prompt_template|model|parser

#App defination
app=FastAPI(title='Langchain server',
            version='1.0',
 descripiton="a simple api sever")


#adding chain routes
add_routes(
    app,
    chain,
    path='/chain'
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)
