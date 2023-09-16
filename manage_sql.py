import sqlite3
from user_auth import UserAuth


class ManageSql:
    """管理数据库的类，打包了一些操作"""

    def __init__(self):
        """初始化数据库的设置"""
        self.db_path = "database.db"

        self.conn = sqlite3.connect(self.db_path)
        # 创建一个游标对象，用于执行SQL语句
        self.cursor = self.conn.cursor()

        # 定义SQL语句以创建表
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            password_hash TEXT,
            salt TEXT, 
            name TEXT
            -- activity_id INTEGER,
            -- FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
            -- age INTEGER,
            -- grade TEXT
        );

        CREATE TABLE IF NOT EXISTS activities (
            activity_id TEXT PRIMARY KEY,
            activity_name TEXT,
            volunteer_hours FLOAT,
            activity_info TEXT 
        );
        
        CREATE TABLE IF NOT EXISTS student_activities (
            student_activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            activity_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
        );

        '''

        # 执行SQL语句以创建表
        self.cursor.executescript(create_table_query)

        # 提交更改
        self.conn.commit()

    def register(self, student_data=("00220001", "hashed_password", "salt_value", "John Doe")):
        """把输入插入到数据库"""

        # 执行INSERT语句
        self.cursor.execute(
            "INSERT INTO students (student_id, password_hash, salt, name) VALUES (?, ?, ?, ?)",
            student_data)

        # 提交更改
        self.conn.commit()

    def activity_add(self, activity_data=("testID", "testNAME", "testHOUR", "testINFO")):
        """把输入插入到数据库"""

        # 执行INSERT语句
        self.cursor.execute(
            "INSERT INTO activities (activity_id, activity_name, volunteer_hours, activity_info) VALUES (?, ?, ?, ?)",
            activity_data)

        # 提交更改
        self.conn.commit()

    def query(self, table="students", key="student_id", value_to_check: str = "00220001"):
        """查询某键的值是否存在于表中，默认在表students中查询学号是否存在"""
        # 执行查询
        self.cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {key} = ?", (value_to_check,))
        result = self.cursor.fetchone()

        # 检查查询结果
        if result[0] > 0:
            print(f"键{key}的值{value_to_check}存在于表{table}中")
            return True, result
        else:
            print(f"键{key}的值{value_to_check}不存在于表{table}中")
            return False, result

    def close(self):
        self.conn.close()
