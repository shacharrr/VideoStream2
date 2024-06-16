import aiosqlite
import asyncio

class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name

    async def ConnectDataBase(self):
        try:
            db = await aiosqlite.connect(self.db_name)
            c = await db.cursor()

            await c.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT, watch_history TEXT, favorites TEXT);''')
            await c.execute('''CREATE TABLE IF NOT EXISTS videos
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, views INTEGER, review TEXT, genre TEXT, rating INTEGER);''')
            await db.commit()
            return db
        except Exception as e:
            print(e)
            return None
        
    async def InsertUser(self, email, username, password):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()
            await c.execute(f"INSERT INTO users (email, username, password) VALUES (?, ?, ?);", (email, username, password))
            await db.commit()
            await db.close()
        except Exception as e:
            print(e)
            return None
        
    async def GetUserByEmail(self, email):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()
            await c.execute(f"SELECT * FROM users WHERE email = ?;", (email,))
            user = await c.fetchone()
            await db.close()
            return user
        except Exception as e:
            print(e)
            return None
        
    async def InsertVideo(self, name, review, genre, rating, _id=None):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()
            if _id == None:
                await c.execute(f"INSERT INTO videos (name, views, review, genre, rating) VALUES (?, 0, ?, ?, ?);", (name, review, genre, rating))
            else:
                await c.execute(f"INSERT INTO videos (id, name, views, review, genre, rating) VALUES (?, ?, 0, ?, ?, ?);", (_id, name, review, genre, rating))
            await db.commit()
            await db.close()
        except Exception as e:
            print(e)
            return None

    async def GetVideoById(self, key, update_views = True):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()

            if update_views:
                await c.execute(f"UPDATE videos SET views = views + 1 WHERE id = ?;", (key,))
                await db.commit()

            await c.execute(f"SELECT * FROM videos WHERE id = ?;", (key,))
            video = await c.fetchone()
            await db.close()
            return video
        except Exception as e:
            print(e)
            return None
        
    async def GetAllVideosContaining(self, query):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()
            await c.execute(f"SELECT * FROM videos WHERE name LIKE ? OR genre LIKE ?;", (query, query))
            videos = await c.fetchall()
            await db.close()
            return videos
        except Exception as e:
            print(e)
            return None
        
    async def AddWatchHistoryToUser(self, user, key):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()

            await c.execute(f"SELECT watch_history FROM users WHERE username = ?;", (user,))
            watch_history = await c.fetchone()
            if watch_history[0] == None:
                watch_history = ""
            else:
                if watch_history[0].count(",") > 4:
                    watch_history = watch_history[0].split(",")[1:]
                    watch_history = ",".join(watch_history)
                watch_history = f"{watch_history[0]},"
            
            query = watch_history + key
            await c.execute(f"UPDATE users SET watch_history = ? WHERE username = ?;", (query,user))
            await db.commit()
            await db.close()
        except Exception as e:
            print(e)
            return None
        
        
    async def GetWatchHistoryByUser(self, query):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()
            await c.execute(f"SELECT watch_history FROM users WHERE email = ?;", (query,))
            watch_history = await c.fetchone()
            await db.close()
            return watch_history
        except Exception as e:
            print(e)
            return None
        
    async def AddFavoriteToUser(self, user, key):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()

            await c.execute(f"SELECT favorites FROM users WHERE username = ?;", (user,))
            favorites = await c.fetchone()
            if favorites[0] == None:
                favorites = ""
            else:
                favorites = f"{favorites[0]},"
            
            query = favorites + key
            await c.execute(f"UPDATE users SET favorites = ? WHERE username = ?;", (query,user))
            await db.commit()
            await db.close()
        except Exception as e:
            print(e)
            return None
        
    async def GetFavoritesByUser(self, query):
        try:
            db = await self.ConnectDataBase()
            c = await db.cursor()
            await c.execute(f"SELECT favorites FROM users WHERE email = ?;", (query,))
            favorites = await c.fetchone()
            await db.close()
            return favorites
        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    db = DataBase('storage/database.db')
    asyncio.run(db.ConnectDataBase())