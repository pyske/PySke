def run_tests(tests, filename = ""):
	for f in tests:
		try :
			f()
			print("\033[32m[OK] " +str(f)[10:][:-16] + " (test/"+str(filename) +".py)\033[0m")
		except Exception as e:
			print("\033[31m[KO] " +str(f) + " (test/"+str(filename) +".py)\033[0m")
			print(e)