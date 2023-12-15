from collections import Counter
import json
from bs4 import BeautifulSoup
import numpy as np
import requests
from exceptions import UrlError
import re

class RawPage:
    """
    Represents a raw web page with attributes for URL, data, and headline.

    Attributes:
        url (str): The URL address of the article.
        _data (str): Private attribute to store the downloaded content of the page.
        _headline (str): Private attribute to store the headline of the page.

    Methods:
        __init__(self, url):
            Initializes a RawPage instance with the provided URL, setting data and headline to None.

        _fetch_data(self):
            Private method to fetch and populate data and headline attributes from the web page.

        data(self) -> str:
            Getter property for the data attribute. Downloads and returns the page content when accessed.

        headline(self) -> str:
            Getter property for the headline attribute. Downloads and returns the page headline when accessed.

    Example:
        >>> page = RawPage("https://en.wikipedia.org/wiki/Python_(programming_language)")
        >>> print(page.data)
        # Output: (downloads and returns page content)
        >>> print(page.headline)
        # Output: (downloads and returns page headline)
    """
    def __init__(self, url):
        """
        Initializes a RawPage instance with the provided URL, setting data and headline to None.

        Parameters:
            url (str): The URL address of the article.
        """
        self.url = url
        self._data = None
        self._headline = None

    @property
    def data(self):
        """
        Getter property for the data attribute. Downloads and returns the page content when accessed.
        """
        if self._data is None:
            self._fetch_data()
        return self._data

    @property
    def headline(self):
        """
        Getter property for the headline attribute. Downloads and returns the page headline when accessed.
        """
        if self._headline is None:
            self._fetch_data()
        return self._headline

    def _fetch_data(self):
        """
        Private method to fetch and populate data and headline attributes from the web page.
        Raises UrlError for invalid URLs.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            headline_element = soup.find('h1', {'id': 'firstHeading'})
            self._headline = headline_element.text if headline_element else "Headline not found"

            self._data = soup

        except requests.exceptions.RequestException as e:
            raise UrlError(self.url, f"Failed to fetch data: {str(e)}")

class PageContent:
    """
    Represents the content of a web page with attributes for sentences and words.

    Attributes:
        url (str): The URL address of the page.
        sentences (list): A list of sentences extracted from the page content.
        words (list): A list of words extracted from the page content.

    Methods:
        __init__(self, url):
            Initializes a PageContent instance with the provided URL, setting sentences and words to None.

        get_sentences(self) -> list:
            Getter method to retrieve the list of sentences.

        get_words(self) -> list:
            Getter method to retrieve the list of words.

        set_sentences(self, attr):
            Setter method to set the sentences attribute.

        set_words(self, attr):
            Setter method to set the words attribute.

    Example:
        >>> content = PageContent("https://example.com")
        >>> sentences = content.get_sentences()
        >>> words = content.get_words()
        >>> print(sentences)
        # Output: None
        >>> print(words)
        # Output: None
    """
    def __init__(self, url):
        """
        Initializes a PageContent instance with the provided URL, setting sentences and words to None.

        Parameters:
            url (str): The URL address of the page.
        """
        self.url = url
        self.sentences = None
        self.words = None
    
    def get_sentences(self) -> list:
        """
        Getter method to retrieve the list of sentences.
        """
        return self.sentences
    
    def get_words(self) -> list:
        """
        Getter method to retrieve the list of words.
        """
        return self.words

    def set_sentences(self, attr):
        """
        Setter method to set the sentences attribute.

        Parameters:
            attr (list): List of sentences to set.
        """
        self.sentences = attr

    def set_words(self, attr):
        """
        Setter method to set the words attribute.

        Parameters:
            attr (list): List of words to set.
        """
        self.words = attr

class Extractor:
    """
    Extractor class responsible for extracting sentences and words from a RawPage and populating a PageContent instance.

    Attributes:
        sentences (list): List to store extracted sentences.
        words (list): List to store extracted words.

    Methods:
        __init__(self):
            Initializes an Extractor instance with sentences and words set to None.

        extract_sentences(self, raw_page: RawPage, page_content: PageContent):
            Extracts sentences from the provided RawPage and sets them in the given PageContent instance.

        extract_words(self, raw_page: RawPage, page_content: PageContent):
            Extracts words from the provided RawPage and sets them in the given PageContent instance.

        _fetch_data(self, raw_page: RawPage):
            Private method to fetch and populate sentences and words attributes from the RawPage.

    Example:
        >>> extractor = Extractor()
        >>> raw_page = RawPage("https://example.com")
        >>> page_content = PageContent("https://example.com")
        >>> extractor.extract_sentences(raw_page, page_content)
        >>> print(page_content.get_sentences())
        # Output: (list of extracted sentences)
        >>> extractor.extract_words(raw_page, page_content)
        >>> print(page_content.get_words())
        # Output: (list of extracted words)
    """
    def __init__(self):
        """
        Initializes an Extractor instance with sentences and words set to None.
        """
        self.sentences = None
        self.words = None
    
    def extract_sentences(self, raw_page: RawPage, page_content: PageContent):
        """
        Extracts sentences from the provided RawPage and sets them in the given PageContent instance.

        Parameters:
            raw_page (RawPage): The RawPage instance to extract sentences from.
            page_content (PageContent): The PageContent instance to set extracted sentences.
        """
        if self.sentences is None:
            self._fetch_data(raw_page)
        page_content.set_sentences(self.sentences)

    def extract_words(self, raw_page: RawPage, page_content: PageContent):
        """
        Extracts words from the provided RawPage and sets them in the given PageContent instance.

        Parameters:
            raw_page (RawPage): The RawPage instance to extract words from.
            page_content (PageContent): The PageContent instance to set extracted words.
        """
        if self.words is None:
            self._fetch_data(raw_page)
        page_content.set_words(self.words)

    def _fetch_data(self, raw_page: RawPage):
        """
        Private method to fetch and populate sentences and words attributes from the RawPage.

        Parameters:
            raw_page (RawPage): The RawPage instance to extract data from.
        """
        # Extract text content from 'p' tags in the RawPage
        texts = [sentence.text for sentence in raw_page.data.find_all('p')]

        # Split text into sentences using a simple approach
        sentence_endings = re.compile(r'[.!?]')
        self.sentences = [sentence.strip() for text in texts for sentence in sentence_endings.split(text) if sentence.strip()]

        # Populate the words attribute
        self.words = [word for sentence in self.sentences for word in sentence.split()]


class PageAnalytics:
    """
    PageAnalytics class responsible for analyzing the content of a PageContent and generating analytics data.

    Attributes:
        page_content (PageContent): The PageContent instance to be analyzed.
        analytics_data (dict): Dictionary to store the analytics results.

    Methods:
        __init__(self, page_content):
            Initializes a PageAnalytics instance with the provided PageContent and generates analytics data.

        make_analytics(self):
            Analyzes the content of the PageContent and populates the analytics_data dictionary.

        save_to_json(self, filename: str):
            Saves the analytics_data to a JSON file with the specified filename.

        __str__(self) -> str:
            Returns a string representation of the PageAnalytics instance.

    Example:
        >>> page_content = PageContent("https://example.com")
        >>> analytics = PageAnalytics(page_content)
        >>> print(analytics)
        # Output: (string representation of analytics results)
        >>> analytics.save_to_json("analytics_results.json")
        # Saves analytics data to "analytics_results.json" file.
    """
    def __init__(self, page_content):
        """
        Initializes a PageAnalytics instance with the provided PageContent and generates analytics data.

        Parameters:
            page_content (PageContent): The PageContent instance to be analyzed.
        """
        self.page_content = page_content
        self.analytics_data = {}
        self.make_analytics()

    def make_analytics(self):
        """
        Analyzes the content of the PageContent and populates the analytics_data dictionary.
        """
        words = self.page_content.get_words()

        # Calculate the top 20 most frequent words
        word_freq_top20 = dict(Counter(words).most_common(20))

        # Filter out stopwords
        stopwords = {'and', 'or', 'but', 'in', 'on', 'at', 'with', 'for', 'the', 'a'}
        filtered_word_freq = {word: freq for word, freq in word_freq_top20.items() if word.lower() not in stopwords}

        # Select the top 10 from the original dictionary
        top_10_word_freq = dict(sorted(word_freq_top20.items(), key=lambda x: x[1], reverse=True)[:10])

        # Select the top 10 most frequent words without considering prepositions and conjunctions
        top_10_filtered_word_freq = dict(sorted(filtered_word_freq.items(), key=lambda x: x[1], reverse=True)[:10])

        # Save the results
        self.analytics_data['top_10_words'] = top_10_word_freq
        self.analytics_data['top_10_words_filtered'] = top_10_filtered_word_freq

        # Calculate average and median word length
        word_lengths = np.array([len(word) for word in words])
        self.analytics_data['average_word_length'] = np.mean(word_lengths)
        self.analytics_data['median_word_length'] = np.median(word_lengths)

        # Calculate the top 10 longest words
        longest_words = sorted(words, key=len, reverse=True)[:10]
        longest_words_dict = {word: len(word) for word in longest_words}
        self.analytics_data['top_10_longest_words'] = longest_words_dict

        # Calculate average and median sentence length
        sentences = self.page_content.get_sentences()
        sentence_lengths = np.array([len(sentence.split()) for sentence in sentences])
        self.analytics_data['average_sentence_length'] = np.mean(sentence_lengths)
        self.analytics_data['median_sentence_length'] = np.median(sentence_lengths)
        
        # Find and store the longest sentence
        longest_sentence = max(sentences, key=lambda sentence: len(sentence.split()))
        self.analytics_data['longest_sentence'] = longest_sentence

    def save_to_json(self, filename: str):
        """
        Saves the analytics_data to a JSON file with the specified filename.

        Parameters:
            filename (str): The name of the JSON file to save the analytics data.
        """
        self.analytics_data['url'] = self.page_content.url
        with open(filename, 'w') as json_file:
            json.dump(self.analytics_data, json_file, indent=2)

    def __str__(self) -> str:
        """
        Returns a string representation of the PageAnalytics instance.
        """
        output = f"Page Analytics for {self.page_content.url}\n"
        output += f"Top 10 Words: {self.analytics_data['top_10_words']}\n"
        output += f"Top 10 Words (No Stopwords): {self.analytics_data['top_10_words_filtered']}\n"
        output += f"Average Word Length: {self.analytics_data['average_word_length']:.2f}\n"
        output += f"Median Word Length: {self.analytics_data['median_word_length']:.2f}\n"
        output += f"Top 10 Longest Words: {self.analytics_data['top_10_longest_words']}\n"
        output += f"Average Sentence Length: {self.analytics_data['average_sentence_length']:.2f}\n"
        output += f"Median Sentence Length: {self.analytics_data['median_sentence_length']:.2f}\n"
        output += f"The longest Sentence: {self.analytics_data['longest_sentence']:.2f}\n"
        return output

