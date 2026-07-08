test:
	python3 testes.py

clean:
	rm -rf __pycache__ tests/__pycache__

docker-build:
	docker build --platform linux/amd64 -t atv08-comp .

docker-test: docker-build
	docker run --rm --platform linux/amd64 atv08-comp

.PHONY: test clean docker-build docker-test
