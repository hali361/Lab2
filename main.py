
def load_stopwords(file_path: str) -> set:
    with open(file_path, 'r') as file:
        stop_words = set(file.read().lower().split())
        print(f"Loaded stop words: {len(stop_words)}")
    return stop_words

def filter_stopwords(text: str, stop_words: set) -> list:
    words = [word.strip('.,') for word in text.split()]
    filtered_words = [word.lower() for word in words if word and word.lower() not in stop_words]
    return filtered_words

def calculate_term_frequency(frequency: dict, total_words: int) -> dict:
    return {
        word: round(count / total_words, 4)
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
        open('data/textA.txt', 'r') as file_a,
        open('data/textB.txt', 'r') as file_b,
    ):
        stop_words = load_stopwords('data/stopwords.txt')
        text_a = file_a.read()
        text_b = file_b.read()

    #filter stop words from both texts
    filtered_text_a = filter_stopwords(text_a, stop_words)
    filtered_text_b = filter_stopwords(text_b, stop_words)

    #will use later to calculate relative frequency
    total_words_a = len(filtered_text_a)
    total_words_b = len(filtered_text_b)

    #calculate term frequency of key words in both texts
    term_freq_a = calculate_term_frequency({word: filtered_text_a.count(word) for word in dict.fromkeys(filtered_text_a)}, total_words_a)
    term_freq_b = calculate_term_frequency({word: filtered_text_b.count(word) for word in dict.fromkeys(filtered_text_b)}, total_words_b)


    #extract words that are unique to each text (in one, but not in both)
    ##we are able to use the frequency of unique words in each text to calculate the relative frequency of those same words.
    unique_freq_a, unique_freq_b, non_unique_words = extract_unique_words(term_freq_a, term_freq_b)
    unique_term_freq_a, unique_term_freq_b = {
        word: term_freq_a[word]
        for word in unique_freq_a
    }, {
        word: term_freq_b[word]
        for word in unique_freq_b
    }

    print("Filtered Document A (excluding stop words):")
    print(filtered_text_a)

    print("Filtered Document B (excluding stop words):")
    print(filtered_text_b)

    print("\nTerm frequency of words in Document A (excluding stop words):")
    print(term_freq_a)

    print("\nTerm frequency of words in Document B (excluding stop words):")
    print(term_freq_b)

    #printing of unique words and their frequencies
    print("\nWords that occur in both documents:")
    print(non_unique_words)

    print("\nTerm frequency of words unique to Document A (excluding stop words):")
    print(unique_term_freq_a)

    print("\nTerm frequency of words unique to Document B (excluding stop words):")
    print(unique_term_freq_b)
main()