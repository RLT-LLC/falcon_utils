class MongoConnectionMiddleware:
    def __init__(self, motor):
        self.motor = motor

    async def process_startup(self, scope, event):
        self.motor.connect()

    async def process_shutdown(self, scope, event):
        self.motor.disconnect()
