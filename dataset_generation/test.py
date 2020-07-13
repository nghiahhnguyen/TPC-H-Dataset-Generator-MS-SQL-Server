from gen_equivalent_showplans import create_filtered_queries, extract_clauses

with open("../dbgen/generated_queries/train/13/0.sql") as f:
	s = f.read()
	print('\n==='.join(extract_clauses(s)))
