import sqlite3
import re
from collections import Counter
from string import punctuation
from math import sqrt
from pathlib import Path
from typing import Optional, List, Tuple, Dict

class Chatbot:
    """
    Core chatbot engine for learning and generating responses using an SQLite database.
    """

    def __init__(self, db_path: str):
        """
        Initialize the chatbot engine with a path to the SQLite database.

        - Establishes a connection to the SQLite database at the given path.
        - Creates a cursor for executing SQL commands.
        - Ensures that the required tables (words, sentences, associations) exist in the database.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)  # Connect to SQLite database file
        self.cursor = self.connection.cursor()           # Create a cursor for database operations
        self._ensure_db_schema()                         # Ensure tables are created

    def _ensure_db_schema(self):
        """
        Ensure the database schema is present.

        - Creates the 'words', 'sentences', and 'associations' tables if they do not already exist.
        - 'words': stores unique words.
        - 'sentences': stores unique sentences and a usage counter.
        - 'associations': links words to sentences with a weight indicating association strength.
        """
        create_table_requests = [
            'CREATE TABLE IF NOT EXISTS words(word TEXT UNIQUE)',  # Table for unique words
            'CREATE TABLE IF NOT EXISTS sentences(sentence TEXT UNIQUE, used INT NOT NULL DEFAULT 0)',  # Table for unique sentences and usage count
            'CREATE TABLE IF NOT EXISTS associations (word_id INT NOT NULL, sentence_id INT NOT NULL, weight REAL NOT NULL)'  # Table for word-sentence associations
        ]
        for request in create_table_requests:
            self.cursor.execute(request)  # Execute each CREATE TABLE statement
        self.connection.commit()          # Commit changes to the database

    def _get_id(self, entity: str, text: str) -> int:
        """
        Retrieve the rowid for a word or sentence, inserting it if not present.

        Args:
            entity: Either 'word' or 'sentence'.
            text: The word or sentence to look up.

        Returns:
            The rowid of the word or sentence in its respective table.

        - Checks if the word/sentence exists in the database.
        - If it exists, returns its rowid.
        - If not, inserts it and returns the new rowid.
        """
        table = entity + 's'  # Table name: 'words' or 'sentences'
        column = entity       # Column name: 'word' or 'sentence'
        self.cursor.execute(f'SELECT rowid FROM {table} WHERE {column} = ?', (text,))
        row = self.cursor.fetchone()
        if row:
            return row[0]  # Return existing rowid if found
        self.cursor.execute(f'INSERT INTO {table} ({column}) VALUES (?)', (text,))
        self.connection.commit()
        return self.cursor.lastrowid  # Return new rowid after insertion

    def _get_words(self, text: str) -> List[Tuple[str, int]]:
        """
        Tokenize the input text into words and punctuation, returning a list of (word, count) tuples.

        Args:
            text: The input string to tokenize.

        Returns:
            A list of tuples, each containing a word/punctuation and its count in the text.

        - Uses a regular expression to split the text into words and punctuation.
        - Converts text to lowercase for normalization.
        - Counts occurrences of each token.
        """
        words_regexp = re.compile(r'(?:\w+|[' + re.escape(punctuation) + r']+)')  # Regex for words and punctuation
        words_list = words_regexp.findall(text.lower())  # Tokenize and lowercase
        return list(Counter(words_list).items())         # Count occurrences

    def learn(self, bot_message: str, user_response: str) -> None:
        """
        Learn from the user's response to the bot's message by updating associations in the database.

        Args:
            bot_message: The message sent by the bot.
            user_response: The user's reply to the bot.

        - Tokenizes the bot's message into words and counts their occurrences.
        - Calculates the total weighted length of the words for normalization.
        - Gets or inserts the user's response as a sentence in the database.
        - For each word in the bot's message:
            - Gets or inserts the word in the database.
            - Calculates the association weight (importance of the word in the message).
            - Inserts an association between the word and the user's response.
        - Commits all changes to the database.
        """
        words = self._get_words(bot_message)  # Tokenize bot message
        words_length = sum(n * len(word) for word, n in words) or 1  # Weighted length for normalization
        sentence_id = self._get_id('sentence', user_response)        # Get or insert user response
        for word, n in words:
            word_id = self._get_id('word', word)                     # Get or insert word
            weight = sqrt(n / float(words_length))                   # Calculate association weight
            self.cursor.execute(
                'INSERT INTO associations (word_id, sentence_id, weight) VALUES (?, ?, ?)',
                (word_id, sentence_id, weight)
            )
        self.connection.commit()                                     # Commit changes

    def get_response(self, user_input: str) -> str:
        """
        Generate a response to the user's input based on learned word-sentence associations.

        Args:
            user_input: The input string from the user.

        Returns:
            The most relevant response sentence, or a fallback if no associations exist.

        - Tokenizes the user input and calculates word frequencies.
        - For each word, computes a weight based on its frequency and length.
        - Creates a temporary table to accumulate association scores for candidate sentences.
        - For each word, inserts into the results table all sentences associated with that word,
          adjusting the score by association weight and sentence usage (to promote variety).
        - Selects the sentence with the highest total score as the response.
        - If no associations are found, selects the least-used sentence at random.
        - If the database is empty, returns a default message.
        - Increments the usage count for the selected sentence.
        - Commits changes and returns the selected response.
        """
        words = self._get_words(user_input)  # Tokenize user input
        words_length = sum(n * len(word) for word, n in words) or 1  # Weighted length for normalization

        # Create a temporary table to store candidate sentences and their scores
        self.cursor.execute('CREATE TEMPORARY TABLE results(sentence_id INT, sentence TEXT, weight REAL)')
        for word, n in words:
            weight = sqrt(n / float(words_length))  # Calculate word weight
            self.cursor.execute(
                '''
                INSERT INTO results
                SELECT associations.sentence_id, sentences.sentence,
                       ? * associations.weight / (4 + sentences.used)
                FROM words
                INNER JOIN associations ON associations.word_id = words.rowid
                INNER JOIN sentences ON sentences.rowid = associations.sentence_id
                WHERE words.word = ?
                ''',
                (weight, word)
            )
        # Aggregate scores for each candidate sentence and select the best one
        self.cursor.execute(
            'SELECT sentence_id, sentence, SUM(weight) AS sum_weight FROM results GROUP BY sentence_id ORDER BY sum_weight DESC LIMIT 1'
        )
        row = self.cursor.fetchone()
        self.cursor.execute('DROP TABLE results')  # Clean up temporary table
        if row is None:
            # Fallback: select the least-used sentence at random
            self.cursor.execute(
                'SELECT rowid, sentence FROM sentences WHERE used = (SELECT MIN(used) FROM sentences) ORDER BY RANDOM() LIMIT 1'
            )
            row = self.cursor.fetchone()
            if row is None:
                return "I don't know what to say yet."  # No sentences in database
        # Increment usage count for the selected sentence
        self.cursor.execute('UPDATE sentences SET used = used + 1 WHERE rowid = ?', (row[0],))
        self.connection.commit()
        return row[1]  # Return the selected response

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()
