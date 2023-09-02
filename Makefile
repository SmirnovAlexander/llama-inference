LINE_WIDTH=120
ISORT_FLAGS=--line-width=${LINE_WIDTH} --profile black
BLACK_FLAGS=--skip-string-normalization --line-length=${LINE_WIDTH}

install-format:
	pip install black isort

format:
	isort ${ISORT_FLAGS} --check-only --diff .
	black ${BLACK_FLAGS} --check --diff .

format-fix:
	isort ${ISORT_FLAGS} .
	black ${BLACK_FLAGS} .
