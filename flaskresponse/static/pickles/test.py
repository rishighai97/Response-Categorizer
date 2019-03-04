import pickle
with open("accepted_comments.pickle", "rb") as fp:
	b = pickle.load(fp)
print(b)
