from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langserve import add_routes
from decouple import config
from redis import Redis
import helpers

API_KEY_HEADER = "X-API-KEY"
API_ACCESS_USER = config("API_ACCESS_USER")
API_ACCESS_KEY = config("API_ACCESS_KEY")

app = FastAPI()
redis_instance = Redis(
  host=config("REDIS_HOST", cast=str),
  port=config("REDIS_PORT", cast=str, default=6379),
  password=config("REDIS_PASSWORD", cast=str),
  ssl=True
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    rate_limit = 5
    rate_window = 10
    api_key = request.headers.get(API_KEY_HEADER)
    if api_key is None:
        return JSONResponse(status_code=400, content={"detail": "Invalid API Key"})
    
    if api_key != API_ACCESS_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid API Key"}) 

    rate_limit_key = f"rate_limit:{API_ACCESS_USER}"
    rl_current_value = redis_instance.get(rate_limit_key)
    if rl_current_value is None: 
        redis_instance.set(rate_limit_key, 0, rate_window) 
    redis_instance.incr(rate_limit_key)
    final_val = redis_instance.get(rate_limit_key)
    do_rate_limiting = False
    try:
        do_rate_limiting = int(final_val) > rate_limit
    except:
        pass
    if do_rate_limiting:
        return JSONResponse(content={"error": "Rate Limited"}, status_code=429)

    # for future work
    access_total_key = f"api_access: total"
    access_current_value = redis_instance.get(access_total_key)
    if access_current_value is None: 
        redis_instance.set(access_total_key, 0) 
    redis_instance.incr(access_total_key)   

    response = await call_next(request)
    return response



@app.get('/')
def home_page():
    return {"hello": "world"}

chain = helpers.get_chain()
add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app, host='localhost', port=8100)
