import re
import sqlite3

db_path = r'd:\0Study\xlab\study\project\backend\data\private-blog.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

BAD_CHARS = re.compile('[\u200b\u200c\u200d\u2060\u2061\u2062\u2063\ufeff\u00a0\u2028\u2029\u2066\u2067\u2068\u2069\u206a\u206b\u206c\u206d\u206e\u206f\u202a\u202b\u202c\u202d\u202e]')

def clean(text):
    if not text:
        return text
    return BAD_CHARS.sub('', text)

# Articles
rows = conn.execute('SELECT id, content, summary, title FROM articles').fetchall()
for r in rows:
    new_content = clean(r['content'])
    new_summary = clean(r['summary'])
    new_title = clean(r['title'])
    if new_content != r['content'] or new_summary != r['summary'] or new_title != r['title']:
        conn.execute('UPDATE articles SET content=?, summary=?, title=? WHERE id=?',
                     (new_content, new_summary, new_title, r['id']))
        print(f"Article {r['id']}: cleaned")

# Quick posts
rows = conn.execute('SELECT id, content FROM quick_posts').fetchall()
for r in rows:
    new_content = clean(r['content'])
    if new_content != r['content']:
        conn.execute('UPDATE quick_posts SET content=? WHERE id=?', (new_content, r['id']))
        print(f"QuickPost {r['id']}: cleaned")

# Comments
rows = conn.execute('SELECT id, content FROM comments').fetchall()
for r in rows:
    new_content = clean(r['content'])
    if new_content != r['content']:
        conn.execute('UPDATE comments SET content=? WHERE id=?', (new_content, r['id']))
        print(f"Comment {r['id']}: cleaned")

conn.commit()
conn.close()
print('Done.')