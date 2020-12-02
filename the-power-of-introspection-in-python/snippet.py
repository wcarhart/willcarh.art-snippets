def jsonize(self):
	variables = [var for var in dir(self) if not var.startswith(('_', '__')) and not callable(getattr(self, var))]
	return "{" + ",".join([f"\"{var}\": \"{getattr(self, var)}\"" for var in variables]) + "}"