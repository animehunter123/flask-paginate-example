$ErrorActionPreference=0
write-host -fore green "Make sure you have your venv|poetry environment ready, and pip3 install -r ./requirements.txt before proceeding."

write-host -fore yellow "Press Ctrl+C or enter to continue to Cancel..."
Read-Host

write-host "Blowing away old database and cache files..."
rm -Recurse -force .\__pycache__ -ea 0 | out-null
rm -Recurse -force .\migrations  -ea 0 | out-null
rm -Recurse -force .\data.sqlite -ea 0 | out-null

write-host "Running Flask Db SQLITE initialization commands: flask db init ; flask db migrate -m 'initial db' ; flask db upgrade"
flask db init ; flask db migrate -m 'initial db' ; flask db upgrade