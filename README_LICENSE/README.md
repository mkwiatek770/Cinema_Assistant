# Cinema_Assistant
This app will manages all things related with movies field. User can search movies buy tickets and check stats of cinemas.

## Instalation 
* Clone repository on your local computer
* create virtualenv   virtualenv -p python3 venv 
* install all required packages pip install -r requirements.txt
* If you don't have psql install it by typing: 
apt-get install psql
* Restore backup of db, go into database direcotry and write: psql -U postgres -f c_assistant.sql -h 127.0.0.1 cinema_assistant 
* To run flask app go into: app_dir directory and write: python3 run.py

## Usage
This project has many features like: 
* adding a new movie into database 
* buying a ticket to some movie
* generate pdf report of cinema stats like: income, total selled tickets etc.
* gerate xls document with many userfull informations like income, average selled tickets etc. 
* See repertoire of cinemas with many informations like: price, total number of seats, unocuppated seats, required minumum age, title etc.

## Contributing 
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author 
* Michał Kwiatek contact: michalkwiatek8@o2.pl

## License
MIT[https://choosealicense.com/licenses/mit/]

