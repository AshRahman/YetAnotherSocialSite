First we isolated the virtual environment using the below command 

py -3 -m venv venv 

then we uppdated the interpreter to the newly created venv

then we activate the venv by using below command

venv\Scripts\activate

incase of script being disabled in the system use the below command in powershell

Set-ExecutionPolicy RemoteSigned


Then we install fastAPI using

 pip install "fastapi[all]"

 for viewing and installing all the packages required for the project we can use
venv\bin\python -m pip freeze > requirements.txt
INSERTNEWENVIRONMENT\bin\python -m pip install -r requirements.txt

we start the server by using the below command in terminal

uvicorn  main:app

uvicorn  main:app --reload    ----> this is for continuous auto reload


Special note: FastAPI looks for first match in the API calls,so order matters while writing


using postman for testing API calls

in postman go to Body thgen choose the JSON by choosing raw
then type any thing you want to send it to the dictionary inside the function of API
check the console in vscode to see te content


Auto documentation 
http://127.0.0.1:8000/docs#/ 
http://127.0.0.1:8000/redoc

create app folder to keep all the files

created __init__.py file to packages

modify the start server command

uvicorn  app.main:app --reload


POSTGRES Troubleshooting:
cant insert rows---->didnt specify primary key,so the coloumns were read only

POSTGRES driver

pip install psycopg2


SQLALCHEMY for ORM
pip install sqlalchemy

Create a new file called database.py
in there 

Remember to properly import 
code was not running for importing wrong modules

creating schemas file and adding the shcema modules
creating seperate classes for more control

creating routers to split up path operations

using APIRouter fro routing the files

using prefix to reduce the path length like /posts---->/

JWT Tokens--------------------

 