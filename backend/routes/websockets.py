from fastapi import WebSocket,APIRouter,HTTPException,WebSocketDisconnect,WebSocketException,status
from dependencies.auth import get_current_user
from auth.jwt_token import get_ws_payload
from socket_manager.manager import manager

ws = APIRouter(prefix="/ws")

@ws.websocket('/')
async def create_websocket(websocket : WebSocket):
    payload = get_ws_payload(websocket)
    is_loggedin = get_current_user(payload)
    if not is_loggedin:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Unauthorized"
        )
    await websocket.accept()
    manager.add_sockets(is_loggedin,websocket)
    try:
        await websocket.receive_text()
    except WebSocketDisconnect:
        manager.remove_socket(is_loggedin)