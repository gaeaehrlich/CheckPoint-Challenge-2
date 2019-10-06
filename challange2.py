import os
import hashlib


def extract_leafs_hash(folder_path, sub_hash):
    for filename in os.listdir(folder_path):
        file_num = int((filename.split('_'))[1])
        filename = os.path.join(folder_path, filename)
        file = open(filename, "rt")
        text = file.readline()
        sub_hash[file_num] = hashlib.md5(text.encode())


def tx_root(folder_path, height, sons):
    sub_hash = [None] * pow(sons, height)
    extract_leafs_hash(folder_path, sub_hash)
    for l in range(height, 0, -1):
        sons_offset = pow(sons, (height - l))
        chunks_offset = pow(sons, (height - l) + 1)
        chunks = pow(sons, l) // sons
        for j in range(chunks):
            concat = ''
            for k in range(sons):
                concat += sub_hash[chunks_offset*j + sons_offset*k].hexdigest()
            sub_hash[j*chunks_offset] = hashlib.md5(concat.encode())
    return sub_hash[0]


def calc_tx_roots(directory, tx_roots):
    for folder in sorted(os.listdir(directory)):
        folder_path = os.fsdecode(folder)
        path = folder_path.split('-')
        block = path[0].split('_')
        block_num = int(block[1])
        height = path[1].split('_')
        sons = path[2].split('_')
        tx_roots[block_num] = tx_root(folder_path, int(height[1]), int(sons[1])).hexdigest()


def calc_blocks_hash(tx_roots, block_hash):
    prev_hash = 'a861f335d4d457a7c1d00640da380dc4'
    for i in range(16):
        concat = prev_hash + tx_roots[i]
        block_hash[i] = hashlib.md5(concat.encode())
        prev_hash = block_hash[i].hexdigest()


tx_roots = [None]*16
directory = os.fsencode('C:\\Projects\\checkpoint\\blocks')
calc_tx_roots(directory, tx_roots)
block_hash = [None]*16
calc_blocks_hash(tx_roots, block_hash)
print(block_hash[15].hexdigest())



