from app import app
from app.view import updater 


if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
    app.run()