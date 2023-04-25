from typing import List, Dict

import os
import random
import re

from collections import defaultdict

def replace_spaces(data: str) -> str:
    data = re.sub('[\n\r\t\\s]+', ' ', data)
    return data

def load_dataset(path: str) -> str:
    with open(path, 'rt') as fin:
        data = fin.read().lower()

    data = replace_spaces(data)
    return data

def calculate_frequencies(text: str, ngram: int):
    c = defaultdict(float)
    for i in range(0, len(text) - ngram + 1):
        key = text[i : i+ngram]
        c[key] += 1

    total = sum(c.values())
    for key in c:
        c[key] /= total

    return c

def encrypt(message, alphabet):
    key = list(alphabet)
    random.shuffle(key)
    translation_table = str.maketrans(alphabet, ''.join(key))
    return message.translate(translation_table)

def decrypt_based_on_frequencies(message, frequencies, ngram):
    dict_sorted_freqs = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    message_frequencies = calculate_frequencies(message, ngram)
    sorted_message_freqs = sorted(message_frequencies.items(), key=lambda x: x[1], reverse=True)

    translation_table = {}
    for dict_freq, message_freq in zip(dict_sorted_freqs, sorted_message_freqs):
        dict_symbol = dict_freq[0]
        message_symbol = message_freq[0]

        translation_table[message_symbol] = dict_symbol

    decrypted_message = []
    prev_freq = None
    for i in range(0, len(message) + ngram - 1):
        symbol = message[i : i+ngram]
        if not symbol in translation_table:
            prev_freq = None
            continue

        decrypted_symbol = translation_table[symbol]
        decrypted_freq = frequencies[decrypted_symbol]

        letters = list(decrypted_symbol)
        if prev_freq and len(letters) > 1:
            if decrypted_freq > prev_freq:
                decrypted_message = decrypted_message[:-1]

        decrypted_message += letters
        prev_freq = decrypted_freq

    decrypted_message = ''.join(decrypted_message)
    return decrypted_message

def accuracy(message, decrypted_message):
    correct = 0
    for x, y in zip(message, decrypted_message):
        if x == y:
            correct += 1
    return correct / len(message)


class MCMCDecoder:
    def __init__(self, train_data, alphabet):
        self.alpabet = alphabet

        self.train_dict = defaultdict(float)
        for i in range(len(train_data) - 1):
            c0 = train_data[i]
            c1 = train_data[i+1]
            self.train_dict[(c0, c1)] += 1

        for c0 in alphabet:
            for c1 in alphabet:
                self.train_dict[(c0, c1)] += 1

        norm = len(train_data) - 1 + len(alphabet)**2
        for k in self.train_dict.keys():
            self.train_dict[k] /= norm

    def new_permutation(self) -> Dict[str, str]:
        alphabet = list(self.alpabet).copy()
        random.shuffle(alphabet)
        key = {c0:c1 for c0, c1 in zip(self.alpabet, alphabet)}
        return key

    def decode_with_permutation(self, text: str, permutation: Dict[str, str]) -> List[str]:
        decoded = [permutation[c] for c in text]
        return decoded

    def transition_probs(self, text0: List[str], text1: List[str]) -> float:
        if len(text0) != len(text1):
            raise ValueError(f'lengths must be equal: text0: {len(text0)}, text1: {len(text1)}')

        def prob(text, i):
            c0 = text[i]
            c1 = text[i+1]
            p = self.train_dict[(c0, c1)]
            return p

        ratio = 1
        for i in range(len(text0) - 1):
            p0 = prob(text0, i)
            p1 = prob(text1, i)
            ratio *= p0 / p1

        return ratio


    def decode(self, message: str, num_permutations_per_decode=10000, num_attempts=100) -> str:
        best_decoded_message = list(message)

        for _ in range(num_attempts):
            permutation = self.new_permutation()

            for _ in range(num_permutations_per_decode):
                c0, c1 = random.choices(list(permutation.keys()), k=2)

                decoded_message = self.decode_with_permutation(message, permutation)

                permutation[c0], permutation[c1] = permutation[c1], permutation[c0]
                decoded_message_replaced = self.decode_with_permutation(message, permutation)

                ratio = self.transition_probs(decoded_message_replaced, decoded_message)
                if ratio < random.uniform(0, 1):
                    permutation[c1], permutation[c0] = permutation[c0], permutation[c1]

            decoded_message = self.decode_with_permutation(message, permutation)
            ratio = self.transition_probs(decoded_message, best_decoded_message)
            if ratio > 1:
                best_decoded_message = decoded_message

        return ''.join(best_decoded_message)

def main():
    text_en = load_dataset('WarAndPeaceEng.txt')

    ngram = 1

    frequencies_wp_en = calculate_frequencies(text_en, ngram)

    alphabet_en = 'abcdefghijklmnopqrstuvwxyz'
    special_symbols = '0123456789.,-!? '

    alphabet = alphabet_en + special_symbols

    message = """
        Last week, the social media company first made the announcement about saying that
        the label provides more transparency into the company’s process for reducing the reach of hateful tweets.
        “Restricting the reach of Tweets helps reduce binary ‘leave up versus take down’ content moderation decisions
        and supports our freedom of speech vs freedom of reach approach,” the company said at that time.
    """

    message = replace_spaces(''.join([a for a in message.lower() if a in alphabet]))

    print(f'original message: {message}')
    encrypted = encrypt(message, alphabet)
    print(f'encrypted message: {encrypted}')

    decrypted = decrypt_based_on_frequencies(message, frequencies_wp_en, ngram)
    print(f'decrypted frequencies: ngram: {ngram}: {decrypted}')
    print(f'accuracy: {accuracy(message, decrypted):0.2f}')

    train_text = text_en
    decoder = MCMCDecoder(train_text, alphabet)
    decrypted = decoder.decode(encrypted)

    print(f'decrypted mcmc: {decrypted}')
    print(f'accuracy: {accuracy(message, decrypted):0.2f}')

if __name__ == '__main__':
    main()
