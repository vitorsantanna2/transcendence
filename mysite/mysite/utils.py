def insertDirectoryPath(base, path , type):
	destiny = []
	for app in base:
		temp = path / app / type
		if temp.exists():
			destiny.append(temp)
	return destiny
	