# flask-paginate-example
Just a quick demo of how to show 5 results per page (of a example list)

Updated to requiring LOGGING in before you can see the randomly generated results.

To prepare your environment and run this properly I recommend doing it this way:
```
pip3 install virtualenv # or use "pip" instead of pip3
python -m virtualenv venv
./venv/sources/activate

ls # You will now see just the code, but no database file nor migrations

# This will install flask_login, flask_pagination, into your python virtual environment
pip3 install -r ./requirements.txt  

flask db init ; flask db migrate -m 'initial db' ; flask db upgrade

ls # You will now see just the code AND a EMPTY SQLITE database file and migrations folder

python3 app.py

Now go to the webpage, and you will see that the green navbar doesnt have the "Results" link...

Now click Register, make a login, and login... and the Results link will appear

Click Results and a paginated (5 random letters per page) list will appear!!!
```

![image](https://user-images.githubusercontent.com/42163211/231369020-d68c45b3-e1c2-491f-9e10-bcd564bbf615.png)
