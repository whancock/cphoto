

stop_words = ['a', 'the', 'an', 'some', 'and']

location_words = ['above', 'in', 'outside', 'left', 'right', 'wearing', 'riding', 'inside']

def parse(query):

	tokens = query.split()
	tokens = [token for token in tokens if not token in stop_words]
	return tokens

def isAction(keyword):
	return keyword in location_words