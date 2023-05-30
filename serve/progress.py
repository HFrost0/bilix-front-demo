import asyncio
import json
from bilix.progress.cli_progress import CLIProgress


class WebSocketProgress(CLIProgress):
    def __init__(self, sockets):
        super().__init__()
        self._sockets = sockets

    async def broadcast(self, msg: str):
        cors = [s.send_text(msg) for s in self._sockets]
        await asyncio.gather(*cors)

    async def add_task(self, **kwargs):
        task_id = await super().add_task(**kwargs)
        asyncio.create_task(
            self.broadcast(json.dumps({'method': 'add_task', 'task_id': task_id, 'description': kwargs['description']}))
        )
        return task_id

    async def update(self, task_id, **kwargs) -> None:
        await super().update(task_id, **kwargs)
        data = {'method': 'update', "task_id": task_id}
        if 'total' in kwargs:
            data = {**data, 'total': kwargs['total']}
        elif 'advance' in kwargs:
            data = {**data, 'advance': kwargs['advance']}
        data = json.dumps(data)
        asyncio.create_task(self.broadcast(data))
