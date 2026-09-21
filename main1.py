# This is the main program
# write your program here
def remove_stop_words(text: str, stop_words: set) -> list:
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words

def calculate_frequency(text: list) -> dict:
    frequency = {}
    for word in text:
        frequency[word.lower()] = frequency.get(word.lower(), 0) + 1
    return frequency

def extract_unique_words(frequency_a: dict, frequency_b: dict) -> tuple[dict, dict]:
    unique_a = {
        word: count
        for word, count in frequency_a.items()
        if word not in frequency_b
    }
    unique_b = {
        word: count
        for word, count in frequency_b.items()
        if word not in frequency_a
    }
    return unique_a, unique_b

def main():
    with open('stopwords.txt', 'r') as file:
        data = file.read()
        stop_words = set(data.splitlines())

    with open('TextA.txt', 'r') as input_file:
        text = input_file.read()
    filtered_text = remove_stop_words(text, stop_words)

    with open('TextB.txt', 'r') as input_file_b:
        text_b = input_file_b.read()
    filtered_text_b = remove_stop_words(text_b, stop_words)

    frequency_a = calculate_frequency(filtered_text)
    frequency_b = calculate_frequency(filtered_text_b)

    print("Frequency of words in TextA.txt (excluding stop words):")
    for word, freq in frequency_a.items():
        print(f"{word}: {freq}")

    print("\nFrequency of words in TextB.txt (excluding stop words):")
    for word, freq in frequency_b.items():
        print(f"{word}: {freq}")

    rel_freq_a = {word: freq / sum(frequency_a.values()) for word, freq in frequency_a.items()}
    rel_freq_b = {word: freq / sum(frequency_b.values()) for word, freq in frequency_b.items()}

    print("\nRelative frequency of words in TextA.txt (excluding stop words):")
    for word, rel_freq in rel_freq_a.items():
        print(f"{word}: {rel_freq:.4f}")

    print("\nRelative frequency of words in TextB.txt (excluding stop words):")
    for word, rel_freq in rel_freq_b.items():
        print(f"{word}: {rel_freq:.4f}")

    unique_freq_a, unique_freq_b = extract_unique_words(frequency_a, frequency_b)
    unique_rel_freq_a, unique_rel_freq_b = {word: freq / sum(unique_freq_a.values()) for word, freq in unique_freq_a.items()}, {word: freq / sum(unique_freq_b.values()) for word, freq in unique_freq_b.items()}

    print("\nRelative frequency of words unique to TextA.txt (excluding stop words):")
    for word, rel_freq in unique_rel_freq_a.items():
        print(f"{word}: {rel_freq:.4f}")

    print("\nRelative frequency of words unique to TextB.txt (excluding stop words):")
    for word, rel_freq in unique_rel_freq_b.items():
        print(f"{word}: {rel_freq:.4f}")

main()