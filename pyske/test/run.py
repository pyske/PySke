# def run_tests(tests):
# 	for f in tests:
# 		f()

def run_tests(tests):
	for f in tests:
		try :
			f()
			print("\033[32m[OK] " +str(f) + "\033[0m")
		except Exception:
			print("\033[31m[KO] " +str(f)+ "\033[0m")