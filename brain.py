def getRecyclingLabel(labels):
	for label in labels:
		# If we have a 60% confidence it's recyclable
		if label["score"] > .60:
			return label["type"]
	return None