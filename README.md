# Simple WebSocket Notification System using Django and Redis

## Overview
This project is a real-time notification system built with Django Channels, WebSockets, and Redis. The project leverages asynchronous communication for sending and receiving messages between clients and the server using WebSockets. It includes Django’s admin panel to generate notifications and an HTTP-triggered WebSocket process that sends multiple payloads over a single request.

### Features:
- Real-time notifications using WebSocket.
- Sync and async consumers.
- Connection management (connect, send payload, and disconnect).
- Django Admin integration for generating notifications.
- Multiple payloads sent from a single HTTP request.

---

## Installation Guide

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/simple-websocket-django.git
   cd simple-websocket-django
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and configure Redis**:
   Ensure Redis is installed and running:
   ```bash
   redis-server
   ```

5. **Update settings.py**:
   Ensure Redis configuration:
   ```python
   CHANNEL_LAYERS = {
       'default': {
           'BACKEND': 'channels_redis.core.RedisChannelLayer',
           'CONFIG': {
               "hosts": [('127.0.0.1', 6379)],
           },
       },
   }
   ```

---

## Running the Project

1. **Run the Django development server**:
   In one terminal:
   ```bash
   python manage.py runserver
   ```

2. **Run Daphne for ASGI support**:
   In another terminal:
   ```bash
   daphne -p 8001 core.asgi:application
   ```

   This sets up the ASGI server to handle WebSocket connections.

---

## Code Breakdown

### 1. **consumers.py**: WebSocket Consumer

- **AsyncWebSocketConsumer**: Manages WebSocket connections asynchronously for efficient real-time communication.

```python
class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "test_consumer_group"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'status': 'Data received!'}))

    async def disconnect(self, *args, **kwargs):
        print("Disconnected")
```

- **Sync handling**: In `views.py`, we use `async_to_sync` to send data to the WebSocket from synchronous code. This is crucial for triggering WebSocket messages from a traditional Django HTTP request.

### 2. **views.py**: Triggering WebSocket Payloads
When the `home()` view is triggered, multiple payloads are sent over a single HTTP request using a loop and delay mechanism:
```python
def home(request):
    for i in range(1, 10):
        channel_layer = get_channel_layer()
        data = {"count": i}
        async_to_sync(channel_layer.group_send)(
            "test_consumer_group",
            {"type": "send_notification", "value": json.dumps(data)},
        )
        time.sleep(2)
    return HttpResponse()
```
This setup allows a single HTTP request to initiate multiple WebSocket notifications over time.

### 3. **Admin Notifications**
- Notifications are generated from the Django admin interface by creating entries in the `Notification` model.
- On saving a new notification, the model’s `save()` method broadcasts the count of unseen notifications via WebSocket:
```python
async_to_sync(channel_layer.group_send)(
    'test_consumer_group', {
        'type': 'send_notification',
        'value': json.dumps(data)
    }
)
```

---

## WebSocket Workflow

1. **Connecting**: A client connects to the WebSocket via the `/ws/test/` route.
   - This is defined in `asgi.py` under `ws_patterns`.

2. **Sending Payload**: The payload is sent when the `home()` view is triggered, broadcasting messages with incrementing counters to all connected clients.

3. **Generating Notifications**: Admin users can create new notifications via the default Django admin panel, which triggers WebSocket updates.

4. **Disconnecting**: The `disconnect` method in the consumer ensures clean disconnection from the WebSocket when the client disconnects.

---

## Testing

### Screenshots

1. **WebSocket Connection Example**:
   ![WebSocket Connection](assets/1)

2. **Notification Generated via Django Admin**:
   ![Notification Example](relative/path/to/screenshot2.png)

### Redis Management with Brew

To manage Redis as a background service, you can use the following commands:

- Start Redis:
  ```bash
  brew services start redis
  ```
- Restart Redis:
  ```bash
  brew services restart redis
  ```
- Stop Redis:
  ```bash
  brew services stop redis
  ```

Ensure Redis is running before starting your WebSocket and Django servers.

---

### Starting the Servers

For this project to run correctly, you need to start two servers in parallel:

1. **Daphne Server**: This is the ASGI server handling WebSocket connections. Open a terminal and run:
   ```bash
   daphne -p 8001 core.asgi:application
   ```

2. **Django Development Server**: This is the server for HTTP requests, running separately from the WebSocket connection. In a second terminal, run:
   ```bash
   python manage.py runserver
   ```

### Important:
- Both servers need to be started simultaneously, each in its own terminal window. 
- Daphne handles WebSocket connections (on port 8001 in this case), while the `runserver` command manages HTTP traffic on the default port (8000).

  Here's how you can add the explanation of using `uvicorn` as an alternative to `daphne` in your GitHub documentation:

---

### Using `uvicorn` as an Alternative to `daphne`

While this project uses `daphne` to serve the ASGI application, you can alternatively use `uvicorn`, which is another ASGI server commonly used in Django Channels projects. `uvicorn` is known for its speed and lightweight nature, making it a great alternative for handling WebSocket connections.

To use `uvicorn`:

1. **Install `uvicorn`:**
   You can install `uvicorn` via pip:
   ```bash
   pip install uvicorn
   ```

2. **Start the ASGI server using `uvicorn`:**
   Instead of running `daphne` or `python manage.py runserver`, you can start the server using `uvicorn` with the following command:
   ```bash
   uvicorn core.asgi:application --host 127.0.0.1 --port 8001
   ```
   This command will run the ASGI application defined in `core.asgi`.

3. **Run the Django management server**:
   In another terminal, run the Django development server as usual:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

This way, `uvicorn` will handle WebSocket connections on port `8001`, while Django serves regular HTTP requests on port `8000`. Make sure both servers are running simultaneously for full functionality.





3. **Using WebSocket Client (like WebSocket King)**:
   - Connect to `ws://127.0.0.1:8001/ws/test/` for testing the WebSocket connection.
   - View real-time updates sent from the `home()` view and the admin panel.

---

## Conclusion
This project demonstrates how to integrate WebSockets in a Django application for real-time notification updates. The mix of sync and async methods ensures efficient communication, making it scalable for various use cases.
