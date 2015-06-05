def print_result(temp_result, output):
    """
        Writes a SNPposition file to stdoutput
    """
    output.write(str(temp_result) + '\n')
    for line in temp_result:
        output.write(str(line) + '\n')

