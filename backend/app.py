from flask import Flask

app = Flask(__name__, template_folder = "../frontend/templates", static_folder = "../frontend/static")

@app.route('/')
def home():
    return {"message": "Welcome to the prototype backend!"}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
