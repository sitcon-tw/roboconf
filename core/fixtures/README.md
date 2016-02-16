Generate fixtures
-----------------

	python manage.py dumpdata auth.group --indent=4 --natural-foreign

Note: dumpdata generates 5 lines (fat!) for each permission, shift-v the lines and use `:'<,'>global/^/normal 5J` to merge each permissions into one line.
