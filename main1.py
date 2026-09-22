
def load_stopwords(file_path: str) -> set:
    with open(file_path, 'r') as file:
        stop_words = set(file.read().lower().splitlines())
    return stop_words

def remove_stopwords(text: str, stop_words: set) -> list:
    words = [word.strip('.,') for word in text.split()]
    filtered_words = [word for word in words if word and word.lower() not in stop_words]
    return filtered_words


def calculate_frequency(text: list) -> dict:
    frequency = {}
    for word in text:
        word = word.lower()
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def calculate_relative_frequency(frequency: dict, total_words: int) -> dict:
    return {
        word: count / total_words
        for word, count in frequency.items()
    }


def extract_unique_words(frequency_a: dict, frequency_b: dict) -> tuple[dict, dict, set]:
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

    non_unique_words = set(frequency_a.keys()).intersection(set(frequency_b.keys()))
    
    return unique_a, unique_b, non_unique_words


def main():
    with (
        open('data/TextA.txt', 'r') as file_a,
        open('data/TextB.txt', 'r') as file_b,
    ):
        stop_words = load_stopwords('data/stopwords.txt')
        text_a = file_a.read()
        text_b = file_b.read()

    #will use later to calculate relative frequency
    total_words_a = len(text_a.split())
    total_words_b = len(text_b.split())

    #filter stop words from both texts
    filtered_text_a = remove_stopwords(text_a, stop_words)
    filtered_text_b = remove_stopwords(text_b, stop_words)

    #calculate frequency of 'key' words in both texts
    frequency_a = calculate_frequency(filtered_text_a)
    frequency_b = calculate_frequency(filtered_text_b)

    print("Frequency of words in TextA.txt (excluding stop words):")
    for word, freq in frequency_a.items():
        print(f"{word}: {freq}")

    print("\nFrequency of words in TextB.txt (excluding stop words):")
    for word, freq in frequency_b.items():
        print(f"{word}: {freq}")

    #calculate relative frequency of key words in both texts
    rel_freq_a = calculate_relative_frequency(frequency_a, total_words_a)
    rel_freq_b = calculate_relative_frequency(frequency_b, total_words_b)

    print("\nRelative frequency of words in TextA.txt (excluding stop words):")
    for word, rel_freq in rel_freq_a.items():
        print(f"{word}: {rel_freq:.4f}")

    print("\nRelative frequency of words in TextB.txt (excluding stop words):")
    for word, rel_freq in rel_freq_b.items():
        print(f"{word}: {rel_freq:.4f}")

    #extract words that are unique to each text (in one, but not in both)
    ##we are able to use the frequency of unique words in each text to calculate the relative frequency of those same words.
    unique_freq_a, unique_freq_b, non_unique_words = extract_unique_words(frequency_a, frequency_b)
    unique_rel_freq_a, unique_rel_freq_b = {
        word: rel_freq_a[word]
        for word in unique_freq_a
    }, {
        word: rel_freq_b[word]
        for word in unique_freq_b
    }

    #printing of unique words and their frequencies
    print("Words that occur in both texts:")
    for word in non_unique_words:
        print(word)

    print("\nFrequency of words unique to TextA.txt (excluding stop words):")
    for word, freq in unique_freq_a.items():
        print(f"{word}: {freq}")

    print("\nFrequency of words unique to TextB.txt (excluding stop words):")
    for word, freq in unique_freq_b.items():        
        print(f"{word}: {freq}")

    print("\nRelative frequency of words unique to TextA.txt (excluding stop words):")
    for word, rel_freq in unique_rel_freq_a.items():
        print(f"{word}: {rel_freq:.4f}")

    print("\nRelative frequency of words unique to TextB.txt (excluding stop words):")
    for word, rel_freq in unique_rel_freq_b.items():
        print(f"{word}: {rel_freq:.4f}")

main()