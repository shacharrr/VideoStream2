import subprocess
import os
import cv2
import sys
# import sqlite3
import asyncio
from db_conn import DataBase

"""
This function is responsible for converting the video file to HLS format.
"""
def convert_to_hls(video_file, folder_name):
    # set current folder to folder_name
    os.chdir(folder_name)
    
    ffmpeg_cmd = [
        'ffmpeg', '-i', video_file, '-c:v', 'libx264', '-hls_time', '3',
        '-hls_list_size', '0', '-hls_segment_filename',
        f'./segment%03d.ts', f'./playlist.m3u8'
    ]
    subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def create_thumbnail(video_file, folder_name):
    
    cap = cv2.VideoCapture(video_file)
    cap.set(cv2.CAP_PROP_POS_MSEC, 3000)
    # frame from middle of the video
    for i in range(100):
        ret, frame = cap.read()
        if not ret:
            return
        
    frame = cv2.resize(frame, (310, 174))
    cv2.imwrite('thumbnail.jpg', frame)
    cap.release()

"""
This function is responsible for creating a new folder with the last id + 1.
"""
def create_folder_new_id():
    # get the last id of the folder
    try:
        last_id = max([int(folder) for folder in os.listdir('storage/videos') if os.path.isdir(f'storage/videos/{folder}')])
    except:
        last_id = 0

    # create a new folder with the last id + 1
    os.mkdir(f'storage/videos/{last_id + 1}')
    return f'storage/videos/{last_id + 1}'    
    

def duplicate_file_to_folder(video_file, folder_name):
    # copy the video file to the folder
    # in windows
    os.system(f'copy {video_file} {folder_name}')

if __name__ == '__main__':
    if sys.argv[1] == "--help":
        print("Usage: ffmpeg.py <path_to_video> <movie_name> <review> <genre (,)> <rating>")
        sys.exit(0)
        
    video_name, video_review, video_genre ,video_rating = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    # con = sqlite3.connect("storage/database.db")
    # cur = con.cursor()
    # cur.execute(f"INSERT INTO videos (name, views, review, genre) VALUES (?, 0, ?, ?);", (video_name, video_review, video_genre))
    db = DataBase('storage/database.db')
    asyncio.run(db.InsertVideo(video_name, video_review, video_genre, video_rating))

    folder = create_folder_new_id()
    video_file = sys.argv[1]
    duplicate_file_to_folder(video_file, folder)
    convert_to_hls(video_file, folder)
    create_thumbnail(video_file, folder)


