import heapq
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)
        merged_node = HuffmanNode(None, left_node.freq + right_node.freq)
        merged_node.left = left_node
        merged_node.right = right_node
        heapq.heappush(heap, merged_node)

    return heap[0]

def build_huffman_codes(node, current_code, huffman_codes):
    if node is None:
        return

    if node.char is not None:
        huffman_codes[node.char] = current_code
        return

    build_huffman_codes(node.left, current_code + "0", huffman_codes)
    build_huffman_codes(node.right, current_code + "1", huffman_codes)

def compress_text(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    huffman_tree = build_huffman_tree(text)
    huffman_codes = {}
    build_huffman_codes(huffman_tree, "", huffman_codes)

    compressed_text = "".join([huffman_codes[char] for char in text])

    # Pad the compressed text to be a multiple of 8 bits
    padding = 8 - (len(compressed_text) % 8)
    compressed_text += '0' * padding

    # Write the Huffman codes and compressed text to the output file
    with open(output_file, 'wb') as file:
        for i in range(0, len(compressed_text), 8):
            byte = compressed_text[i:i+8]
            file.write(bytes([int(byte, 2)]))

    print(f"Compression complete. Compressed file saved as {output_file}")

def decompress_text(input_file, output_file):
    with open(input_file, 'rb') as file:
        compressed_bytes = file.read()

    compressed_text = ''.join(format(byte, '08b') for byte in compressed_bytes)

    huffman_tree = build_huffman_tree(compressed_text)
    current_node = huffman_tree
    decompressed_text = []

    for bit in compressed_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decompressed_text.append(current_node.char)
            current_node = huffman_tree

    decompressed_text = ''.join(decompressed_text)

    with open(output_file, 'w') as file:
        file.write(decompressed_text)

    print(f"Decompression complete. Decompressed file saved as {output_file}")

if __name__ == "__main__":
    input_file = "input.txt"
    compressed_file = "compressed.huff"
    decompressed_file = "decompressed.txt"

    compress_text(input_file, compressed_file)
    decompress_text(compressed_file, decompressed_file)
