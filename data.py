def getFiles(path):
    # Using readlines()
    file1 = open(path, 'r')
    Lines = file1.readlines()
    print("a") 
    count = 0
    fileList = []
    # Strips the newline character
    for line in Lines:
        count += 1
        temp = line.split("/")
        fileList.append(fileList.append(temp[-1]))
        print("Line{}: {}".format(count, line.strip()))
    return(fileList)
