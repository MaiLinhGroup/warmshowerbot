api:
	uvicorn --port 8181 main:app --reload

add:
	pipenv install $(pkg)

rm:
	pipenv uninstall $(pkg)

install:
	pipenv install

.PHONY: api