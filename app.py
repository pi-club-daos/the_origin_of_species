from flask import Flask

app = Flask(__name__)
app.use_reloader=False
app.run()
import routes