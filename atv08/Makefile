test:
	python3 testes.py

clean:
	rm -rf __pycache__ tests/__pycache__ tests/out

docker-build:
	docker build -t atv08-comp .

docker-test: docker-build
	docker run --rm atv08-comp

.PHONY: test clean docker-build docker-test
