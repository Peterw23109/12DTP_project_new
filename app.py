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

def get_groups():
    #how many blank are in each row
    group = []
    blank = [0,1,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,0]

    # giving the data of each row and adding row and blank into the list
    for group_num in range(1, 19):
        row = query_db("""
            SELECT Element.*, state.state AS state_name, category.category AS category_name
            FROM Element
            LEFT JOIN state ON Element.State = state.id
            LEFT JOIN category ON Element.Category = category.id
            WHERE Element.Group_number = ? COLLATE NOCASE
        """, (group_num,)) 
        group.append((row, blank[group_num-1]))

    return group

@app.route('/table', methods=["GET","POST"])
def table():
    target = None
    if request.method == "POST":
        element_id = request.form.get("element")
        target = query_db("""
                    SELECT Element.*, state.state AS state_name, category.category AS category_name
                    FROM Element
                    LEFT JOIN state ON Element.State = state.id
                    LEFT JOIN category ON Element.Category = category.id WHERE Element.Element_name = ? """, (element_id,), one=True)
        
    
    return render_template('table.html',elements=get_groups(),target=target)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('home.html')


@app.route('/calc', methods = ["GET","POST"])





def calc():

    if request.method == "POST":
        element_list = []
        compound_name = request.form.get("compound")
        print(compound_name)
        i = 0
        while i < len(compound_name):
            i += 1
            symbol = compound_name[i]
            if i < len(compound_name) and compound_name[i].islower():
                symbol += compound_name[i]
                i += 1
            number = ""                     




            element_list.append((symbol, count))

        print(element_list)
        for symbol, count in element_list:
            element = query_db(
                "SELECT Atomic_mass FROM Element WHERE Symbol = ?",
                (symbol,),
                one=True
            )

            if element:
                molar_mass += element["Atomic_mass"] * count
 
    return render_template('gmolcalc.html', molar_mass = molar_mass)


    

if __name__ == "__main__":
    app.run(debug=True)