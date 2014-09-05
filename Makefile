.PHONY: test release doc

test:
	#flake8 sassoclient --ignore=E501,E127,E128,E124 --filename=*.py --exclude=static,migrations
	coverage run --branch --source=sassoclient `which django-admin.py` test sassoclient --settings=sassoclient.tests.test_settings
	coverage report --omit=sassoclient/test*

#release:
#	python setup.py sdist bdist_wheel register upload -s

#doc:
#	cd docs; make html; cd ..
