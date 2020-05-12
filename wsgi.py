from hacktech import app
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gabe/depedantify_google_key.json"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
