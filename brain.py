def getRecyclingLabel(labels):
	for label in labels:
		# If we have a 40% confidence it's recyclable
		if label["score"] > .40:
			return label["type"]
	return None
