from src.parser import parse_string

def parse_file(filename: str, display: bool):
	with open(filename, 'r') as f:
		for line in f:
			parse_string(line, display)

def show_help(program):
	print('Uso:', program, 'archivo', 'display')
	print('\tarchivo: debe ser el nombre del archivo ubicado en ./chalan/tests')
	print("\tdisplay: puede ser true o false, muestra o no la entrada.\n\t\tEs true por defecto.")

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		# Set by default display to True
		display = True

		try:
			if len(argv) >= 3:
				if argv[2] == 'true':
					display = True
				elif argv[2] == 'false':
					display = False
				else:
					raise ValueError(f'{argv[2]} should be either true or false')
		except Exception as e:
			print('Exception:', e)
			show_help(argv[0])
		else:
			parse_file('chalan/tests/' + argv[1], display)
	else:
		show_help(argv[0])
