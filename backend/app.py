from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the trading journal'


if __name__ == '__main__':
    app.run(debug=True)