test:
	python3 testes.py

clean:
	rm -rf __pycache__
	rm -f tests/*.ec1 tests/*.s tests/*.o tests/runtime.s
	find tests/ -type f ! -name "*.*" -delete 2>/dev/null || rm -f tests/teste_[0-9]*

docker-build:
	docker build -t atv06-comp .

docker-test: docker-build
	docker run --rm atv06-comp

.PHONY: test clean docker-build docker-test
