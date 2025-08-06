from collections import Counter
import string

# Load the word list once at startup
def load_words():
    """Load and clean the combined word list."""
    with open("data/filtered_words.txt") as f:
        words = []
        for line in f:
            word = line.strip()
            # Skip explanation lines and ensure word is 5 letters
            if len(word) == 5 and not word.startswith(("Green", "Yellow", "Grey")):
                # Convert to lowercase for consistency
                words.append(word.lower())
    return words

words = load_words()

class WordleSolver:
    # Best starter words based on evaluation
    STARTER_WORDS = ['trace', 'crane', 'stare', 'raise']

    def __init__(self):
        self.stats = {
            'total_games': 0,
            'successful_games': 0,
            'guesses_history': [],
            'word_frequencies': Counter()
        }
        self.reset()

    def reset(self):
        """Reset the game state to start fresh."""
        self.allowed = [set("abcdefghijklmnopqrstuvwxyz") for _ in range(5)]
        self.must_appear = set()
        self.gray_counts = {}
        self.green_positions = {}
        self.green_counts = {}
        self.possible_words = words.copy()
        self.current_guesses = 0
        self.letter_frequencies = self._calculate_letter_frequencies()
        # Don't reset statistics when resetting the game

    def _calculate_letter_frequencies(self):
        """Calculate letter frequencies for each position."""
        freq = [{} for _ in range(5)]
        total_words = len(self.possible_words)
        
        # Count letter frequencies at each position
        for word in self.possible_words:
            for i, letter in enumerate(word):
                freq[i][letter] = freq[i].get(letter, 0) + 1
        
        # Convert to percentages
        for pos_freq in freq:
            for letter in pos_freq:
                pos_freq[letter] = pos_freq[letter] / total_words
                
        return freq

    def score_word(self, word):
        """Score a word based on letter frequencies and uniqueness."""
        score = 0
        used_letters = set()
        
        # Score based on positional letter frequencies
        for i, letter in enumerate(word):
            if letter in self.letter_frequencies[i]:
                score += self.letter_frequencies[i][letter]
            
            # Bonus for unique letters (prioritize words that test more letters)
            if letter not in used_letters:
                score += 0.1
                used_letters.add(letter)
        
        return score

    def get_best_guess(self):
        """Get the best word to guess next."""
        if self.current_guesses == 0 and any(word in self.possible_words for word in self.STARTER_WORDS):
            # Use a pre-determined starter word if available
            for word in self.STARTER_WORDS:
                if word in self.possible_words:
                    return word
        
        # Score all possible words and return the best one
        if not self.possible_words:
            return None
            
        scored_words = [(word, self.score_word(word)) for word in self.possible_words]
        return max(scored_words, key=lambda x: x[1])[0]

    def is_possible(self, word):
        """Check if a word fits the current constraints."""
        word_counter = Counter(word)

        # Check position constraints
        for i, letter in enumerate(word):
            if letter not in self.allowed[i]:
                return False

        # Check that required letters appear
        if not self.must_appear.issubset(word_counter.keys()):
            return False

        # Handle gray letters with special case for letters that appear elsewhere
        for letter, count in self.gray_counts.items():
            if letter in self.green_positions:
                # Letter appears in green positions
                min_count = len(self.green_positions[letter])
                # The word should have exactly the number of green occurrences
                if word_counter.get(letter, 0) < min_count:
                    return False
            elif letter in self.must_appear:
                # Letter appears as yellow somewhere
                if word_counter.get(letter, 0) != 1:  # We know it appears exactly once
                    return False
            else:
                # Letter doesn't appear in green or yellow positions
                if letter in word_counter:
                    return False

        return True

    def filter_words(self):
        """Update the list of possible words based on constraints."""
        self.possible_words = [word for word in self.possible_words if self.is_possible(word)]
        if self.possible_words:
            self.letter_frequencies = self._calculate_letter_frequencies()

    def update_constraints(self, guess, feedback):
        """Update filtering rules based on the latest guess and feedback."""
        self.current_guesses += 1
        self.stats['word_frequencies'][guess] += 1
        guess_green_counts = Counter()

        for i in range(5):
            g_char = guess[i]
            res = feedback[i]

            if res == "green":  # Process greens first
                self.allowed[i] = {g_char}
                self.green_positions.setdefault(g_char, []).append(i)
                guess_green_counts[g_char] += 1
                self.must_appear.add(g_char)

            elif res == "yellow":  # Then yellows
                self.must_appear.add(g_char)
                self.allowed[i].discard(g_char)  # Can't appear in this position

            elif res == "gray":  # Finally grays
                # Only discard from this position if letter appears elsewhere
                if g_char in self.must_appear or g_char in self.green_positions:
                    self.allowed[i].discard(g_char)
                else:
                    # Letter doesn't appear at all, can discard from all positions
                    for j in range(5):
                        self.allowed[j].discard(g_char)
                    # Track gray count for letter frequency constraints
                    self.gray_counts[g_char] = self.gray_counts.get(g_char, 0) + 1

        self.green_counts.update(guess_green_counts)

        # Apply filtering
        self.filter_words()

    def end_game(self, success=True):
        """Record game statistics"""
        self.stats['total_games'] += 1
        if success:
            self.stats['successful_games'] += 1
            self.stats['guesses_history'].append(self.current_guesses)

    def get_statistics(self):
        """Return solver statistics"""
        if not self.stats['guesses_history']:
            return {
                'avg_guesses': 0,
                'success_rate': 0,
                'top_words': [],
                'guess_distribution': {}
            }

        return {
            'avg_guesses': round(sum(self.stats['guesses_history']) / len(self.stats['guesses_history']), 1),
            'success_rate': round((self.stats['successful_games'] / self.stats['total_games']) * 100, 1),
            'top_words': self.stats['word_frequencies'].most_common(5),
            'guess_distribution': Counter(self.stats['guesses_history'])
        }

    def get_possible_words(self):
        """Return the list of possible words."""
        return self.possible_words
