import pandas as pd
from classes import (RawPage, PageContent, 
                     Extractor, PageAnalytics)    

urls = ["https://en.wikipedia.org/wiki/Quantum_computing", "https://en.wikipedia.org/wiki/Biochemistry", "https://en.wikipedia.org/wiki/Mathematical_logic"]
analitics_data = []

for url in urls:
    page_info = RawPage(url)
    page_content = PageContent(url)
    extractor = Extractor()
    extractor.extract_sentences(page_info, page_content)
    extractor.extract_words(page_info, page_content)

    # Create PageAnalytics instance and store analytics data in a dictionary
    page_analytics = PageAnalytics(page_content)
    analytics_dict = {
        "URL": url,
        "Longest Sentence": page_analytics.analytics_data['longest_sentence'],
        "Longest Word": max(page_analytics.analytics_data['top_10_longest_words'], key=page_analytics.analytics_data['top_10_longest_words'].get),
        "Number of Sentences": len(page_analytics.page_content.get_sentences()),
        "Number of Words": len(page_analytics.page_content.get_words())
    }
    analitics_data.append(analytics_dict)

# Create a DataFrame for easy comparison
df = pd.DataFrame(analitics_data)

# Print the DataFrame
print(df)
