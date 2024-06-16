import asyncio
import subprocess
import websockets
import json
import os
import hashlib
import ssl

class WebSocketServer:

    """
    This is the constructor for the WebSocketServer class.
    """
    def __init__(self, database, host, port, ssl):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.connected_clients = {}
        self.database = database

    """
    This function is responsible for starting the server and listening for incoming connections.
    """
    def start(self):
        print(f'Server started on: ws{"s" if self.ssl else ""}://{self.host}:{self.port}')

        if self.ssl:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain("./encryption/server.crt", "./encryption/server.key")
            start_server = websockets.serve(self.handle_client, self.host, self.port, ssl=ssl_context)
        else:
            start_server = websockets.serve(self.handle_client, self.host, self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    """
    This function is responsible for stopping the server and closing all connected clients.
    """
    def stop(self):
        for client in self.connected_clients.values():
            client.close()

    """
    This function is responsible for broadcasting a message to all connected clients.
    """
    async def broadcast(self, message):
        for client in self.connected_clients.values():
            await client.send(message)

    """
    This function is responsible for handling the client connection and managing the communication between the server and the client.
    """
    async def handle_client(self, websocket, path):
        print('New client connected!')
        if id(websocket) in self.connected_clients:
            return

        self.connected_clients[id(websocket)] = websocket
        try:
            async for message in websocket:
                response = await self.parse_message(message)
                print(response)
                await websocket.send(response)
        finally:
            del self.connected_clients[id(websocket)]

    """
    This function is responsible for parsing the incoming messages from the client and calling the appropriate function to handle the request.
    """
    async def parse_message(self, message):
        data = json.loads(message)

        print(f"Received message: {data}")

        match data['type']:
            case 'login_request':
                response = await self.login_request(data['user'])
            case 'signup_request':
                response = await self.signup_request(data['user'])
            case 'video_request':
                response = await self.video_request(data['video'])
            case 'search_request':
                response = await self.search_request(data['search'])
            case 'watch_history_add_request':
                response = await self.watch_history_add_request(data['video'])
            case 'watch_history_get_request':
                response = await self.watch_history_get_request(data['user'])
            case 'favorites_add_request':
                response = await self.favorite_add_request(data['video'])
            case 'favorites_get_request':
                response = await self.favorite_get_request(data['user'])
            case 'upload_request':
                response = await self.upload_request(data["video"])
            case _:
                response = json.dumps({'type': 'error', 'message': 'Invalid request type'})

        print(f"Sending response: {response}")
        
        return response
    
    async def login_request(self, user):
        db_user = await self.database.GetUserByEmail(user['email'])
        if db_user == None:
            return json.dumps({'type': 'login_response', 'success': False})
        print(db_user)
        _, _, user_name, user_password, _, _ = db_user

        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        if hashed_password != user_password:
            return json.dumps({'type': 'login_response', 'success': False})

        return json.dumps({'type': 'login_response', 'success': True, "user": {"email": user['email'], "username": user_name}})
    
    async def signup_request(self, user):
        db_user = await self.database.GetUserByEmail(user['email'])
        if db_user != None:
            return json.dumps({'type': 'signup_response', 'success': False})

        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        await self.database.InsertUser(user['email'], user['username'], hashed_password)
        return json.dumps({'type': 'signup_response', 'success': True})
    
    async def video_request(self, video):
        db_video = await self.database.GetVideoById(video['key'])
        if db_video == None:
            return json.dumps({'type': 'video_response', 'success': False})
        
        video_id, video_name, video_views, video_review, _, video_rating = db_video
        return json.dumps({'type': 'video_response', 'success': True, "video": {"id": video_id, "name": video_name, "views": video_views, "review": video_review, "rating": video_rating}})
    
    async def search_request(self, search):
        db_videos = await self.database.GetAllVideosContaining(f"%{search['query']}%") # Note: This is a SQL injection vulnerability
        if db_videos == None:
            return json.dumps({'type': 'search_response', 'success': False})
        videos = []
        for video in db_videos:
            video_id, video_name, video_views, video_review, video_genre, _ = video
            videos.append({"key": video_id, "name": video_name, "views": video_views, "review": video_review, "genre": video_genre})
        
        return json.dumps({'type': 'search_response', 'success': True, "videos": videos})
    
    async def watch_history_add_request(self, video):
        await self.database.AddWatchHistoryToUser(video['user'], video['key'])
        return json.dumps({'type': 'watch_history_add_response', 'success': True})
    
    async def watch_history_get_request(self, user):
        db_videos = await self.database.GetWatchHistoryByUser(user['email'])
        if db_videos == None or db_videos[0] == None:
            return json.dumps({'type': 'watch_history_get_response', 'success': False})
        videos = []
        video_ids = [int(video_id) for video_id in set(db_videos[0].split(","))]

        for video_id in video_ids:
            db_video = await self.database.GetVideoById(video_id, update_views = False)
            if db_video == None:
                continue
            key, video_name, video_views, video_review, video_genre, _ = db_video
            videos.append({"key": key, "name": video_name, "views": video_views, "review": video_review, "genre": video_genre})
        
        return json.dumps({'type': 'watch_history_get_response', 'success': True, "videos": videos})
    
    async def favorite_add_request(self, video):
        await self.database.AddFavoriteToUser(video['user'], video['key'])
        return json.dumps({'type': 'favorite_add_response', 'success': True})
    
    async def favorite_get_request(self, user):
        db_videos = await self.database.GetFavoritesByUser(user['email'])
        if db_videos == None or db_videos[0] == None:
            return json.dumps({'type': 'favorite_get_response', 'success': False})
        videos = []
        video_ids = [int(video_id) for video_id in set(db_videos[0].split(","))]

        for video_id in video_ids:
            db_video = await self.database.GetVideoById(video_id, update_views = False)
            if db_video == None:
                continue
            key, video_name, video_views, video_review, video_genre, _ = db_video
            videos.append({"key": key, "name": video_name, "views": video_views, "review": video_review, "genre": video_genre})
        
        return json.dumps({'type': 'favorites_get_response', 'success': True, "videos": videos})
    
    async def upload_request(self, video):
        try:
            last_id = max([int(folder) for folder in os.listdir('storage/videos') if os.path.isdir(f'storage/videos/{folder}')])
        except:
            last_id = 0

        os.mkdir(f'storage/videos/{last_id + 1}')
        print(video['data'])

        with open(f"storage/videos/{last_id + 1}/{video["name"]}.mp4", "wb") as f:
            f.write(video['data'])

        cmd = ['py', 'ffmpeg.py', f'storage/videos/{last_id + 1}/{video["name"]}']
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        await self.database.InsertVideo(video['name'])
        return json.dumps({'type': 'upload_response', 'success': True})