from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from aioredis import Redis
from datetime import datetime
from ...utils.db import get_redis_conn


class MessageDTO(BaseModel):
    device_id: int
    content: str


router = APIRouter()


@router.get("/stream")
async def connect_to_stream(response: Response, db: Redis = Depends(get_redis_conn)):
    async def event_stream():
        pubsub = db.pubsub(ignore_subscribe_messages=False)

        await pubsub.subscribe("chat")

        async for message in pubsub.listen():
            if message["type"] == "message":
                event = {
                    "event": "message",
                    "id": "834733b955f677fa",
                    "retry": 9000,
                    "data": message.get("data").decode("utf-8"),
                }
                yield f"event: {event['event']}\ndata: {event['data']}\nid:{event['id']}\n\n"

    # The text/event-stream header tells the client that this connection will be event based
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/message/{channel_id}")
async def add_message(
    channel_id: str, messageDTO: MessageDTO, db: Redis = Depends(get_redis_conn)
):
    """
    Publish a message in the channel with the given id
    """
    last_activity = datetime.utcnow().isoformat()

    await db.hset(f"devices:{messageDTO.device_id}", "last_activity", last_activity)

    await db.publish(channel=channel_id, message=messageDTO.content)

    return JSONResponse(content={"published": True})


@router.get("/message/{device_id}")
async def get_device_info(device_id: int, db: Redis = Depends(get_redis_conn)):
    device = await db.hgetall(f"devices:{device_id}")
    return {"device": device}
