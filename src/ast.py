def transpose(data):
	return list(map(list, zip(*data)))

def range_of(data: list):
	from operator import itemgetter
	results = []

	is_array = type(data[0]) is not list
	if is_array:
		data = [data]

	for matrix in data:
		a = [ i for (i,j) in sorted(enumerate(matrix), key=itemgetter(1))]

		result = [element for _, element in sorted(zip(a, range(1,len(a)+1)))]

		current = None
		i = j = None
		for r in range(1,len(a)+1):
			if current is None:
				current = matrix[result.index(r)]
				i = j = r
				continue

			if current == matrix[result.index(r)]:
				j += 1
			else:
				if j - i > 0:
					val = avg_of([n for n in range(i,j+1)])
					for n in range(i,j+1):
						result[result.index(n)] = val
				current = matrix[result.index(r)]
				i = j = r

		if j - i > 0:
			val = avg_of([n for n in range(i,j+1)])
			for n in range(i,j+1):
				result[result.index(n)] = val
		results.append(result)
	return results if not is_array else results[0]

def avg_of(matrix: list):
	if type(matrix[0]) is list:
		return avg_of([avg_of(m) for m in matrix])
	else:
		return sum(matrix)/len(matrix)

def size_of(matrix):
	if type(matrix[0]) is list:
		return sum([len(m) for m in matrix])
	else:
		return len(matrix)

def friedman(variable: dict):
	n = len(variable['patients'])
	k = len(variable['treatments'])

	sum_R_sqrd = sum([ sum(r)**2 for r in transpose(range_of(variable['patients']))])

	return (12/(n*k*(k+1))*sum_R_sqrd) - 3*n*(k+1)

def dotop(variable):
    print("Operación punto")
    if len(variable) == 4:
        matrix = variable[0]
        i = variable[1]
        j = variable[2]
        k = variable[3]
        rachas, matrixrachas = multicot(matrix)
        print("-----", matrixrachas)
        dotoprachas_result = dotoprachas(matrixrachas, 0,0,0)
        print("----------------", dotoprachas_result)
        lenmatrix = len(matrix)
        for i in range(lenmatrix):
            l = len(matrix[i])
            print(l)
        
    return 0


def dotoprachas(matrixrachas, i, j, k):
    print("matrixrachas", matrixrachas)
    sum_rachas_total = sum(sum(sum(matrixrachas,[]),[]))
    print("as",sum(sum(sum(matrixrachas,[]),[])))
    print("a1",sum(sum(matrixrachas[1],[])))
    print("a2",sum(sum(matrixrachas[:][1],[])))
    print("a3",sum(sum(matrixrachas[1][1],[])))
    if i == j == k == 0:
        pass
    elif i == j == k > 0:
        rachas_ijk = matrixrachas[i][j][k]
    else:
        if i > 0 and (j == k == 0):
            return sum(sum(matrixrachas[i-11],[]))
        elif j > 0 and (i == k == 0):
            return sum(sum(matrixrachas[:][j-1],[]))
        elif i == j > 0 and k == 0:
            return sum(sum(matrixrachas[i-1][j-1],[]))
        else:
            raise KeyError

def multicot(matrix):
    dim1 = len(matrix)
    dims = [len(matrix[i]) for i in range(dim1)]
    print("dims", dims)
    dims2 = []
    for i in range(dim1):
        if i == 0:
            dims2.append(dims[i])
        else:
            dims2.append(dims[i]+dims2[i-1])
        print(i)

    print("dims2", dims2)
    union = sum(matrix, [])
    union.sort()
    mc = funmulticot(union)
    rachas = [1 for i in range(len(mc))]
    if (len(mc) != 0):
        prev = mc[0]
        rachas[0] = 1
        for i in range(1,len(mc)):
            if mc[i] == prev:
                rachas[i] = rachas[i-1]
            else:
                rachas[i] += rachas[i-1]
            prev = mc[i]

    matriznumrachas = []
    for i in range(dim1):
        if i == 0:
            lista = [rachas[:dims2[i]]]
        else:
            lista = [rachas[dims2[i-1]:dims2[i]]]
        matriznumrachas.append(lista)

    return rachas, matriznumrachas

def funmulticot(vector):
    mc = []
    for i in range(len(vector)):
        if vector[i] > 0:
            mc.append(1)
        else:
            mc.append(0)
    return mc

functions = {
	'range': range_of,
	'size' : size_of,
	'avg' : avg_of,
	'friedman': friedman,
    'dotop': dotop,
}

