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
		
		disconnected_users: list[WebSocket] = []
		
		for websocket in self.active_connections:
			try:
				await websocket.send_text(message)
			except WebSocketDisconnect:
				disconnected_users.append(websocket)
				
		for user in disconnected_users:
			self.disconnect(user)
			
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
	try:
		while True:
			await websocket.receive_text()
	except WebSocketDisconnect:
		manager.disconnect(websocket)