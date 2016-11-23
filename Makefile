assignee_keywords.csv:
	python main.py get_assignee_keywords

foo: assignee_keywords.csv
	python main.py load_assignee_keywords
.PHONY: foo

save: assignee_keywords.csv
	python main.py save_matrix
.PHONY: save

interactive: assignee_keywords.csv
	python main.py interactive
.PHONY: interactive
