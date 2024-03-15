#!/usr/bin/python3
# Estrutura a base do instalador toolmux
#

from datetime import datetime
import pymysql
import sqlite3
import dotenv
import os

# Base do instalador
base = 'tools.db'

# Deleta base antiga
if os.path.isfile(base):
  os.system(f"rm {base}")
  
dotenv.load_dotenv()

# Conexão com o mysql
mysql_conn = pymysql.connect(
    host = os.getenv('MYSQL_HOST'), 
    user = os.getenv('MYSQL_USER'), 
    password = os.getenv('MYSQL_PASSWORD'), 
    db = os.getenv('MYSQL_DB'))
mysql_cur = mysql_conn.cursor()

# Conexão com o sqlite
sqlite_conn = sqlite3.connect(base)
sqlite_cur = sqlite_conn.cursor()

# Criar estrutura de tabelas das ferramentas
print("[+] Criando estrutura de tabelas...")
sqlite_cur.executescript("""
CREATE TABLE IF NOT EXISTS author (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  github VARCHAR(100),
  created DATETIME NOT NULL,
  modified DATETIME NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS category (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  created DATETIME NOT NULL,
  modified DATETIME NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS installation_type (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  created DATETIME NOT NULL,
  modified DATETIME NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS situation_tool (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  created DATETIME NOT NULL,
  modified DATETIME NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS tool (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  alias VARCHAR(30) NOT NULL,
  executable VARCHAR(30),
  name_repo VARCHAR(30),
  link VARCHAR(60),
  dependencies VARCHAR(500),
  category_id INTEGER NOT NULL,
  installation_type_id INTEGER NOT NULL,
  tool_author_id INTEGER NOT NULL,
  situation_tool_id INTEGER NOT NULL,
  installation_tip VARCHAR(500),
  description VARCHAR(500),
  created DATETIME NOT NULL,
  modified DATETIME NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY(category_id) REFERENCES category (id),
  FOREIGN KEY(installation_type_id) REFERENCES installation_type (id),
  FOREIGN KEY(situation_tool_id) REFERENCES situation_tool (id),
  FOREIGN KEY(tool_author_id) REFERENCES author (id)
);
""")
sqlite_conn.commit()

# Inserir dados na tabela categories
mysql_cur.execute("USE toolmux;")
mysql_cur.execute("SELECT * FROM category;")

print("[+] Inserindo dados na tabela category...")
for row in mysql_cur.fetchall():
  sqlite_cur.execute(f"INSERT INTO category(name, created) VALUES('{row[1]}', '{datetime.utcnow()}')")
sqlite_conn.commit()

# Inserir dados na tabela installation_types
mysql_cur.execute("SELECT * FROM installation_type;")

print("[+] Inserindo dados na tabela installation_type...")
for row in mysql_cur.fetchall():
  sqlite_cur.execute(f"INSERT INTO installation_type(name, created) VALUES('{row[1]}', '{datetime.utcnow()}')")
sqlite_conn.commit()

# Inserir dados na tabela authors
mysql_cur.execute("SELECT * FROM author;")

print("[+] Inserindo dados na tabela author...")
for row in mysql_cur.fetchall():
  sqlite_cur.execute(f"INSERT INTO author(name, created) VALUES('{row[1]}', '{datetime.utcnow()}')")
sqlite_conn.commit()

# Inserir dados na tabela situationstools
mysql_cur.execute("SELECT * FROM situation_tool;")

print("[+] Inserindo dados na tabela situation_tool...")
for row in mysql_cur.fetchall():
  sqlite_cur.execute(f"INSERT INTO situation_tool(name, created) VALUES('{row[1]}', '{datetime.utcnow()}')")
sqlite_conn.commit()

# Inserir dados na tabela tools
mysql_cur.execute("SELECT * FROM tool;")

print("[+] Inserindo dados na tabela tool...")
for row in mysql_cur.fetchall():
  sqlite_cur.execute(f"INSERT INTO tool(name, alias, executable, name_repo, link, dependencies, category_id, installation_type_id, tool_author_id, situation_tool_id, installation_tip, description, created) VALUES('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}', '{row[11]}', '{row[12]}', '{datetime.utcnow()}')")
sqlite_conn.commit()
sqlite_conn.close()
mysql_conn.close()
