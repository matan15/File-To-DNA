from bitstring import BitArray
import os.path

# A dictionary which represents the 4 DNA bases in bits.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
base_to_bit = {"A": BitArray("0b00").bin, "T": BitArray("0b01").bin, "G": BitArray("0b10").bin,
               "C": BitArray("0b11").bin}


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The main function; responsible for organising the sequence of events: 
# 1) Ask the user to enter file path
# 2) Convert the file to DNA
# 3) Ask the user to enter DNA file path
# 4) Convert the DNA file back to a normal file.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def main():
    while True:
        file_path = input("Enter the path of the file you want to convert into DNA: ")
        dna_path = input("Enter path of the directory in which you want to save your file as DNA sequence: ")
        bits = file_to_bits(file_path)
        if not bits:
            print("I can't find the file... please try entering the path again!")
        else:
            assert not isinstance(bits, bool)
            dna_path += bits_to_dna(bits, dna_path, filename_from_path(file_path))
            break

    print(
        """
The DNA saved in file named: "{}", please don't change its name or location.
\nTo prove you this is really your file, I will ask you to enter the path to the DNA file.
You can play with DNA file; delete some characters here, add some characters there and I will translate it
back to a normal file, this way you'll be able to see how your changes has affected the file.\n
    """.format(dna_path))
    new_filename = fix_file_name(name_and_extension(file_path)[1], input("Enter new file name (without extension): "))
    path_new_file_directory = input("Enter directory's path where you want to save the new file: ")
    print("\nplease wait while I'm converting to file and saving (it may take few minutes)...\n")
    bits_to_file(dna_to_bits(dna_path), new_filename, path_new_file_directory)
    print("Here you go! Look at the directory files, see your new file? Open it!")


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function receives the path of the file as an argument. If the file does not exist the function returns false. If the file does exist, the function returns the bits of the file.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def file_to_bits(file_path):
    try:
        with open(file_path, "rb") as f:
            print("\nPlease wait while I'm converting your file into DNA sequence (it may take few minutes)...\n")
            bits = BitArray().bin
            for line in f.readlines():
                bits += BitArray(line).bin
    except FileNotFoundError:
        return False
    except PermissionError:
        return False
    return bits


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function receives bits, path (where to save the DNA), and the name of the file as arguments. Based on the "DNA-base-to-bits" dictionary, the bits are converted to a DNA sequance, which later gets written in the text file.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def bits_to_dna(bits, path, filename):
    dna = ""
    for i in range(1, int((len(bits) / 2) + 1)):
        for base, val in base_to_bit.items():
            if val == bits[(i - 1) * 2:i * 2]:
                dna += base
    with open(os.path.join(path, ret := (fix_file_name(
            ".txt", name_and_extension(filename)[0] + " (DNA)"))), "w+") as f:
        f.write(dna)
    return ("/" if path != "" else "") + ret


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function receives the path of the DNA file as an argument, reads it, and based on the "DNA-base-to-bits" dictionary, returns it as bits. In addition, the functions also checks if the received file does not contain characters that are not A, C, T ot G. If the file does contain speacial characters, the function will inform the user. If the given path the doesn't exist the function will notify the user as well.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def dna_to_bits(dna_path):
    ret = BitArray().bin
    try:
        with open(dna_path, "r") as f:
            dna = f.read()
            for base in dna:
                if base != "A" and base != "T" and base != "C" and base != "G":
                    print("the given file does not contain a proper DNA sequence, please fix it.")
                    return dna_to_bits(input("Enter the path to file again, after you fixed the sequence: "))
                ret += base_to_bit.get(base)
            return ret
    except FileNotFoundError:
        return dna_to_bits(input("I can't find your file, please enter a new path: "))


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function adds counter (text.txt ([counter])) if a file with the given name already exists and returns the fixed filename with its extension.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def fix_file_name(extension, new_filename):
    counter = 1
    ret = ""
    if os.path.isfile(new_filename + extension):
        while os.path.isfile(fixed := (new_filename + " (" + str(counter) + ")" + extension)):
            counter += 1
        ret = fixed
    else:
        ret += new_filename + extension
    return ret


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function receives bits that had been converted from DNA, new file name that the user want to set, and the path of the directory in which the user want to save its file. the funcion creats the new file in that directory, converting the bits into a normal file and saving it.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def bits_to_file(bits, new_filename, directory_path):
    with open(os.path.join(directory_path, new_filename), "wb+") as f:
        for i in range(1, int(len(bits) / 8) + 1):
            f.write(int(bits[(i - 1) * 8:i * 8], 2).to_bytes(1, 'little'))


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function receives a filename as a parameter and seeks for the delimiter which separates between the filename and its extension. The function returns as a tuple the filename and its extension.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def name_and_extension(filename):
    extension_index = filename.rfind(".")
    return filename[:extension_index], filename[extension_index:]


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# The function receives a path as a parameter and checks to see if the user used "/" or "\"  in its path.
# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
def filename_from_path(path):
    return path[path.rfind("/") + 1:] if path.rfind("/") > path.rfind("\\") else path[path.rfind("\\") + 1:]


# ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

# This if statement runs the program.
if __name__ == '__main__':
    main()
