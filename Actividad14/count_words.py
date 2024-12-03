import re

class CountWords:
    def count(self, s: str) -> int:
        pattern = r'\b[a-zA-Z]+([sS]|[rR]|\'[sS])\b'
        p_words = len(re.findall(pattern, s))
        return p_words