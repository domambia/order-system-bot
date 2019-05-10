from app import app
from app.main import updater 


if __name__ == "__main__":
	updater.start_polling()
	app.run()