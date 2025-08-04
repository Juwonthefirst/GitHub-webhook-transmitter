from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()
queue: asyncio.Queue = asyncio.Queue()

@app.head("/")
@app.get("/")
async def home():
	return {"status": "hello"}


@app.post("/github/push/")
async def github_webhook(): 
	await queue.put("push event")
	#print(await queue.get())
	return {"status": "ok"}
	
async def send_github_push_event():
	while True:
		#print("help starting github push event")
		#data = await queue.get()
		print("event sent")
		yield f"{data} \n\n"
	
@app.get("/event/github/")
async def github_push_event():
	print("user connected")
	return StreamingResponse(send_github_push_event(), media_type = "text/event-stream")
	