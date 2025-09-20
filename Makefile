.PHONY: find run gemini pyright mypy sccli tests

find:
	grep -rl --exclude-dir={.venv,.git,__pycache__,.mypy_cache,.pytest_cache.ruff_cache} $s .

run:
	python main.py

gemini:
	npx https://github.com/google-gemini/gemini-cli

pyright:
	pyright

mypy:
	mypy .

sccli:
	python main.py

tests:
	pytest -v
