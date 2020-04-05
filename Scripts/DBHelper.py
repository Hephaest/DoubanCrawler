import sqlite3


class DBHelper:

    def __init__(self):
        self.conn = sqlite3.connect("myDouBan.db")
        self.cur = self.conn.cursor()

    def create_table(self, table_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS " + table_name +
                         "(uid INT PRIMARY KEY NOT NULL, rating NUMERIC(2,1) NOT NULL);")
        self.submit_commit()

    def create_book_info(self, table_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + "_info"
                                                                      "(uid INT REFERENCES " + table_name + "(uid),"
                                                                                                            "p_rating NUMERIC(3,1) NOT NULL,"
                                                                                                            "f_rating NUMERIC(3,1),"
                                                                                                            "name VARCHAR(50),"
                                                                                                            "author VARCHAR(100),"
                                                                                                            "publisher VARCHAR(30),"
                                                                                                            "date VARCHAR(10),"
                                                                                                            "ISBN VARCHAR(13),"
                                                                                                            "final_rating NUMERIC(3,1),"
                                                                                                            "PRIMARY KEY (uid));")
        self.submit_commit()

    def create_public_comment(self, table_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + "_public"
                                                                      "(p_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                      "uid INT REFERENCES " + table_name + "_info(uid),"
                                                                                                           "name VARCHAR(14) NOT NULL,"
                                                                                                           "comment VARCHAR(350) NOT NULL);")
        self.submit_commit()

    def create_friend_comment(self, table_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + "_friends"
                                                                      "(f_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                      "uid INT REFERENCES " + table_name + "_info(uid),"
                                                                                                           "name VARCHAR(14) NOT NULL,"
                                                                                                           "comment VARCHAR(350) NOT NULL);")
        self.submit_commit()

    def find_uid(self, table_name):
        self.cur.execute("SELECT uid FROM " + table_name + ";")
        return self.cur.fetchall()

    def find_rating(self, table_name, uid):
        self.cur.execute("SELECT p_rating FROM " + table_name + " WHERE uid = " + uid + ";")
        return self.cur.fetchall()

    def add_uid_and_rating(self, table_name, attr1, attr2, value1, value2):
        self.cur.execute("INSERT INTO " + table_name + " (" + attr1 + ", " + attr2 + ") VALUES ("
                         + str(value1) + ", " + str(value2) + ");")

    def add_comment(self, table_name, attr1, attr2, attr3, value1, value2, value3):
        self.cur.execute("INSERT INTO " + table_name + " (" + attr1 + ", " + attr2 + ", " + attr3 + ") VALUES ("
                         + value1 + ", \"" + str(value2) + "\", \"" + value3 + "\");")

    def update_book_detail(self, table_name, attr1, value1, value2, value3, value4, value5, value6, value7):
        self.cur.execute("UPDATE " + table_name + "_info SET f_rating = " + value1 + "," +
                         "name = \"" + value2 + "\"," +
                         "author = \"" + value3 + "\"," +
                         "publisher = \"" + value4 + "\"," +
                         "date = \"" + value5 + "\"," +
                         "ISBN = " + value6 + ", " +
                         "final_rating = " + value7 + " " +
                         "WHERE uid = " + attr1 + ";")

    def check_existence(self, table_name, uid):
        self.cur.execute("SELECT COUNT(" + str(uid) + ") FROM " + table_name + " WHERE uid = " + str(uid) + ";")
        return False if self.cur.fetchall()[0][0] == 0 else True

    def drop_table(self, table_name):
        self.cur.execute("DROP TABLE IF EXISTS " + table_name + ";")
        self.submit_commit()

    def submit_commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def find_ratings_above_7(self, table_name):
        self.create_book_info(table_name)
        self.cur.execute("SELECT uid, rating FROM " + table_name + " WHERE rating >= 7.0 ORDER BY rating DESC;")
        rows = self.cur.fetchall()
        for row in rows:
            self.add_uid_and_rating(table_name + "_info", "uid", "p_rating", row[0], row[1])
        self.submit_commit()

    def find_rating_top_10(self, table_name):
        self.cur.execute("SELECT uid FROM " + table_name + " ORDER BY final_rating DESC LIMIT 10;")
        return self.cur.fetchall()

    def show_book_detail(self, table_name):
        self.cur.execute("SELECT uid, name, p_rating, ISBN FROM " + table_name + ";")
        return self.cur.fetchall()

    def show_book_comment(self, table_name, uid):
        self.cur.execute("SELECT name, comment FROM " + table_name + " WHERE uid = " + uid + ";")
        return self.cur.fetchall()

    @staticmethod
    def replace_escape_symbols(input):
        return str(input).replace("\'", "''").replace("\"", "''")
