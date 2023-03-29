from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
from neo4j import GraphDatabase
import jieba
import sqlite3
from pathlib import Path
from werkzeug.utils import secure_filename
app = Flask(__name__)

# 设置Neo4j连接
uri = "bolt://localhost:7687"
user = "neo4j"
password = "your_password"
driver = GraphDatabase.driver(uri, auth=(user, password))


# 初始化数据库
def init_db():
    if not Path("history.db").is_file():
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("""
        CREATE TABLE history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()
init_db()

# 配置文件上传
pdfs = UploadSet('pdfs', DOCUMENTS)
app.config['UPLOADED_PDFS_DEST'] = 'static/uploads'
configure_uploads(app, pdfs)


def process_question(question):
    # 分词
    tokens = jieba.lcut(question)

    # 构建查询语句
    query = "MATCH (n) WHERE "
    for token in tokens:
        query += f"n.name = '{token}' OR "
    query = query[:-4]  # 移除最后的 " OR "
    query += " RETURN n"

    # 执行查询并解析结果
    with driver.session() as session:
        result = session.run(query)
        answer = ""
        for record in result:
            node = record["n"]
            answer += f"{node['name']}是一个{node['type']}。"

    # 生成回答
    answer = answer.strip()
    if answer:
        # 将问题和答案存入数据库
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("INSERT INTO history (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
        conn.close()

    return answer

# 主页
@app.route("/", methods=["GET", "POST"])
def index():
    default_answer = "请在输入框中输入您的问题。"
    if request.method == "POST":
        question = request.form["question"]
        answer = process_question(question)
        return render_template("index.html", answer=answer)
    return render_template("index.html", answer=default_answer)

# 历史记录
@app.route("/history")
def history():
    # 从数据库中获取历史记录
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT question, answer FROM history")
    records = c.fetchall()
    conn.close()

    return render_template("history.html", records=records)

# pdf上传
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'pdf' in request.files:
        filename = pdfs.save(request.files['pdf'])
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/generate_knowledge_graph')
def generate_knowledge_graph():
    # 在这里添加生成知识图谱的代码
    pass

if __name__ == "__main__":
    app.run(debug=True)