from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
from datetime import datetime

app = FastAPI()

# 初始化留言数据表
def init_db():
    conn = sqlite3.connect("message_data.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        content TEXT,
        create_time TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# 提交留言接口
@app.post("/submit_msg")
async def submit_msg(username: str = Form(...), content: str = Form(...)):
    if not username.strip() or not content.strip():
        return {"code":400, "msg":"姓名和留言不能为空"}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("message_data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(username,content,create_time) VALUES (?,?,?)",
                (username, content, now))
    conn.commit()
    conn.close()
    return {"code":200, "msg":"留言提交成功！"}

# 获取全部留言
@app.get("/get_msg_list")
async def get_msg():
    conn = sqlite3.connect("message_data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages ORDER BY id DESC")
    res = cur.fetchall()
    conn.close()
    return {"list": res}

# 访问首页
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 处理静态文件请求（图片、CSS、JS等）
@app.get("/{file_path:path}")
async def static_files(file_path: str):
    from fastapi.responses import FileResponse
    import os
    
    full_path = os.path.join(".", file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(full_path)
    return {"error": "File not found"}