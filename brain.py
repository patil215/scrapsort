def getRecyclingLabel(labels):
	for label in labels:
		# If we have a 45% confidence it's recyclable
		if label["score"] > .45:
			return label["type"]
	return None
