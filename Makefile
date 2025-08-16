find:
	grep -rl --exclude-dir={.venv,.git,__pycache__} $s .
run:
	python main.py
gemini:
	npx https://github.com/google-gemini/gemini-cli
