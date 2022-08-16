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