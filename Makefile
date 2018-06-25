.PHONY: format test_all test_headers test_args test_form test_json

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

format:
	yapf -irp flask_validate
	yapf -irp tests
	yapf -ip setup.py

test_all:
	./env/bin/python -m tests

test_headers:
	./env/bin/python -m tests test_headers

test_args:
	./env/bin/python -m tests test_args

test_form:
	./env/bin/python -m tests test_form

test_json:
	./env/bin/python -m tests test_json

test_handle_errors:
	./env/bin/python -m tests test_handle_errors