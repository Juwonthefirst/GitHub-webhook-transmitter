from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()
class SocketManager: 
	def __init__(self):
		self.active_connections: list[WebSocket] = []
		
	async def connect(self, websocket:WebSocket): 
		await websocket.accept()
		self.active_connections.append(websocket)
		
	def disconnect(self, websocket: WebSocket):
		self.active_connections.remove(websocket)
		
	async def broadcast(self, message: str):
		for websocket in self.active_connections:
			try:
				await websocket.send_text(message)
			except WebSocketDisconnect:
				self.disconnect(websocket)
			
manager = SocketManager()


@app.head("/")
@app.get("/")
async def home():
	return {"status": "hello"}


@app.post("/github/push/")
async def github_webhook(): 
	await manager.broadcast("push")
	return {"status": "ok"}
	
@app.websocket("/event/github/")
async def github_push_event(websocket:WebSocket):
	await manager.connect(websocket)
	print("connected")