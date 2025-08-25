find:
	grep -rl --exclude-dir={.venv,.git,__pycache__} $s .

run:
	python main.py

gemini:
	npx https://github.com/google-gemini/gemini-cli

pyright:
	pyright

mypy:
	mypy .

sccli:
	python3 main.py
