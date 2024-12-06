from fastapi import FastAPI
import uvicorn
from langserve import add_routes
import helpers

app = FastAPI()

@app.get('/')
def home_page():
    return {'hello': 'world'}

chain = helpers.get_chain()
add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8100)
