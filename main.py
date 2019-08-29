# THIS IS A TESTING FILE FOR RENDERING JINJA2
# WHEN MERGING A BRANCH, DISCARD THIS FILE.
# PLEASE.

from flask import Flask, render_template, send_from_directory, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/admin')
def admin():
    return render_template('admin.jinja', user=dict(name='Bottersnike', admin=True))

@app.route('/main/')
def main():
    return render_template('main.jinja', items=[
        dict(name='Fortnite', desc='the gayest game for 12 year olds', vote=1, score=-5),
        dict(name='Fortnite', desc='the gayest game for 12 year olds', vote=0, score=-5),
        dict(name='Fortnite', desc='the gayest game for 12 year olds', vote=0, score=-5),
        dict(name='Fortnite', desc='the gayest game for 12 year olds', vote=-1, score=-5),
        dict(name='Fortnite', desc='the gayest game for 12 year olds', vote=0, score=-5),
        dict(name='Fortnite', desc='the gayest game for 12 year olds', vote=-1, score=-5),
    ], user=dict(name='Bottersnike', admin=True))

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('assets', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
