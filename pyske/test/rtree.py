#TODO

fcts = []

for f in fcts:
	try :
		f()
		print("\033[32m[OK] " +str(f) + "\033[0m")
	except Exception:
		print("\033[31m[KO] " +str(f)+ "\033[0m")