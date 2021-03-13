import os

def build_tree(entity, indent, is_head, is_tail, result):
	# determine if entity is a directory or file
	files = []
	if os.path.isdir(entity):
		files = os.listdir(entity)

	# keep track of line prefixes
	entity_prefix = '└── ' if is_tail else '├── '
	content_prefix = '    ' if is_tail else '|   '
	if is_head:
		entity_prefix = content_prefix = ''

	# add entity to the output
	result += indent + entity_prefix + os.path.basename(entity) + '\n'

	# if entity is a directory, recurse through its contents
	for index in range(len(files) - 1):
		result = build_tree(os.path.join(entity, files[index]), indent + content_prefix, False, False, result)
	if len(files) > 0:
		result = build_tree(os.path.join(entity, files[-1]), indent + content_prefix, False, True, result)
	return result

def generate_file_tree(entity):
	tree = build_tree(entity, '', True, True, '')
	print(tree)
