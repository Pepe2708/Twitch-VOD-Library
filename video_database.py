import sqlite3

def database_connect():
    conn = sqlite3.connect('video.db')
    return conn

def add_video(video):
    conn = database_connect()
    c = conn.cursor()
    
    c.execute("""INSERT INTO videos VALUES (
        :id,
        :length,
        :date,
        :streamer,
        :category,
        :title,
        :url,
        :done,
        :favorite
    )""", video)

    conn.commit()
    conn.close()

def remove_video(video_id):
    conn = database_connect()
    c = conn.cursor()
    
    c.execute(f"DELETE FROM videos WHERE id = {video_id}")
    conn.commit()

    c.execute(f"UPDATE videos SET id = id - 1 WHERE id > {video_id}")
    conn.commit()
    conn.close()

def get_video_info(sort_by, is_ascending):
    conn = database_connect()
    c = conn.cursor()

    if (is_ascending == 1):
        if (sort_by == "favorite" or sort_by == "date"):
            ascending = "DESC"
        else:
            ascending = "ASC"
    elif (is_ascending == 2):
        if (sort_by == "favorite" or sort_by == "date"):
            ascending = "ASC"
        else:
            ascending = "DESC"
    
    if (sort_by == "0"):
        c.execute(f"SELECT * FROM videos ORDER BY id")
        return c.fetchall()
    else:
        c.execute(f"SELECT * FROM videos ORDER BY {sort_by} COLLATE NOCASE {ascending}")
        return c.fetchall()

def get_video_amount():
    conn = database_connect()
    c = conn.cursor()
    
    c.execute("SELECT * FROM videos")
    return len(c.fetchall())

def update_video_order(video_id, direction):
    conn = database_connect()
    c = conn.cursor()

    c.execute(f"SELECT * from videos WHERE id = {video_id}")
    temp_tuple = c.fetchone()

    video = {
    'id': None,
    'length': None,
    'date': None,
    'streamer': None,
    'category': None,
    'title': None,
    'url': None,
    'done': None,
    'favorite': None
}

    def tuple_to_dict(tuple):
        key_amount = len(list(video.keys()))
        key_list = list(video.keys())
        for i in range(key_amount):
            video[key_list[i]] = tuple[i]

        return video

    video = tuple_to_dict(temp_tuple)

    c.execute(f"DELETE FROM videos WHERE id = {video_id}")
    conn.commit()

    if direction == "top":
        c.execute(f"UPDATE videos SET id = id + 1 WHERE id < {video_id}")
        conn.commit()
        video['id'] = 0
        add_video(video)
    elif direction == "bottom":
        c.execute(f"UPDATE videos SET id = id - 1 WHERE id > {video_id}")
        conn.commit()
        video['id'] = get_video_amount()
        add_video(video)
    
    conn.close()

def toggle_done(video_id):
    conn = database_connect()
    c = conn.cursor()
    
    c.execute(f"SELECT NOT done FROM videos WHERE id = {video_id}")
    boolean = c.fetchone()[0]
    c.execute(f"UPDATE videos SET done = {boolean} WHERE id = {video_id}")
    conn.commit()
    conn.close()

def toggle_favorite(video_id):
    conn = database_connect()
    c = conn.cursor()
    
    c.execute(f"SELECT NOT favorite FROM videos WHERE id = {video_id}")
    boolean = c.fetchone()[0]
    c.execute(f"UPDATE videos SET favorite = {boolean} WHERE id = {video_id}")
    conn.commit()
    conn.close()

def update_duration(video_id, request_body):
    conn = database_connect()
    c = conn.cursor()

    c.execute(f"UPDATE videos SET length = '{request_body.length}' WHERE id = {video_id}")
    
    conn.commit()
    conn.close()