run: 
	python3 SubmissionApiFetcher.py
	python3 testing.py
	python3 app.py

openPostman:
	curl --location 'http://localhost:4000/contest/create' --header 'Content-Type: application/json' --data '{	"name" : "biweekly contest 134"}'