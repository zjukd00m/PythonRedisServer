import uvicorn

APP_PORT = 8080
APP_HOST = "127.0.0.1"


if __name__ == "__main__":
    uvicorn.run("src.server:get_app", port=APP_PORT, host=APP_HOST, factory=True)
