.PHONY: regen test lint build clean help

help:
	@echo "make regen   - apply overlay.yaml to openapi.json, regenerate src/trelis_sdk/"
	@echo "make test    - run pytest"
	@echo "make lint    - run ruff check + format"
	@echo "make build   - build wheel + sdist"
	@echo "make clean   - remove build artifacts and the generated SDK"

regen:
	uv run --with pyyaml python scripts/apply_overlay.py
	mkdir -p src
	rm -rf src/trelis_sdk
	uvx --from openapi-python-client openapi-python-client generate \
		--path build/openapi.merged.json \
		--meta=none \
		--output-path src/trelis_sdk \
		--overwrite \
		--config openapi-python-client.config.yaml
	@echo "Generated src/trelis_sdk/"

test:
	uv run --extra dev pytest

lint:
	uv run --extra dev ruff check src tests
	uv run --extra dev ruff format --check src tests

build:
	uv build

clean:
	rm -rf build dist src/trelis_sdk *.egg-info
