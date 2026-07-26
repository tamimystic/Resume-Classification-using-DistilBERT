import re
from collections import Counter

class SummarizationPipeline:
    def __init__(self):
        self.stop_words = {'the', 'and', 'is', 'in', 'to', 'of', 'it', 'for', 'a', 'on', 'with', 'as', 'by', 'an', 'this', 'that', 'are', 'was', 'were', 'be', 'at', 'or', 'from'}
            
    def summarize(self, text, num_sentences=5):
        if not text or len(text.strip()) == 0:
            return "No text available for summary."
        
        # Split by newlines and punctuation FIRST so messy OCR lists get separated
        text = text.replace('\r', '\n')
        raw_sentences = re.split(r'[.!?\n]+', text)
        
        # Clean each sentence and filter out short fragments
        sentences = [re.sub(r'\s+', ' ', s).strip() for s in raw_sentences]
        sentences = [s for s in sentences if len(s) > 15]
        
        if len(sentences) <= num_sentences:
            return ". ".join(sentences) + "."
            
        words = re.findall(r'\w+', " ".join(sentences).lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        if not words:
            return ". ".join(sentences[:num_sentences]) + "."
            
        freq = Counter(words)
        max_freq = max(freq.values())
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_words = re.findall(r'\w+', sentence.lower())
            if not sentence_words:
                continue
            for w in sentence_words:
                if w in freq:
                    score += freq[w] / max_freq
            sentence_scores[i] = score / (len(sentence_words) + 1)
            
        # Get top exactly `num_sentences` sentences while preserving original order
        top_indices = sorted(sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences])
        
        # strictly maximum 5-6 lines, join with period
        summary = ". ".join([sentences[i].capitalize() for i in top_indices]) + "."
        
        return summary
