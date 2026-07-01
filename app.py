from flask import Flask, g, render_template, request, session, redirect, url_for
import sqlite3

DATABASE = 'element.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():

    group = []
    # how many blank is there each column
    blank = [0,1,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,0]
    
    #add each element into the list and sending the number of blank in each gro
    for group_num in range(1,19):
        row = query_db(""" SELECT Element.*, state.state AS state_name, category.category AS category_name
                            FROM Element
                            LEFT JOIN state ON Element.State = state.id
                            LEFT JOIN category ON Element.Category = category.id
                            WHERE Element.Group_number = ? 
                    """, (group_num,))

            
        group.append((row, blank[group_num-1]))
  
     

        
    return render_template('home.html',elements=group)

if __name__ == "__main__":
    app.run(debug=True)