


def lexical_diversity(text):
	return len(text) / len(set(text))


def word_percentage(word, text):
	return 100 * text.count(word) / len(text)