import heapq
from collections import Counter, namedtuple
import pickle

class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, f, None, None) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix="", codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_compress(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded = ''.join(codes[ch] for ch in text)

    padding = 8 - len(encoded) % 8
    encoded += '0' * padding
    byte_array = bytearray()
    for i in range(0, len(encoded), 8):
        byte_array.append(int(encoded[i:i+8], 2))

    with open(output_path, "wb") as f:
        pickle.dump((byte_array, codes, padding), f)

    return len(text), len(byte_array)

def huffman_decompress(input_path, output_path):
    with open(input_path, "rb") as f:
        byte_array, codes, padding = pickle.load(f)

    bit_string = ''.join(f"{byte:08b}" for byte in byte_array)
    bit_string = bit_string[:-padding]

    reverse_codes = {v: k for k, v in codes.items()}
    decoded, buffer = "", ""
    for bit in bit_string:
        buffer += bit
        if buffer in reverse_codes:
            decoded += reverse_codes[buffer]
            buffer = ""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decoded)

    return len(byte_array), len(decoded)
