import string

from strsimpy.cosine import Cosine
from strsimpy.qgram import QGram

class MyMetric():
    def __init__(self):
        self.cmp = Cosine(4)
        
    def distance(self, s1: str, s2: str):
        assert ' ' in s1
        assert ' ' in s2
        s1_tokens = s1.split(' ')
        s2_tokens = s2.split(' ')
        
        avg_len = np.mean((len(s1_tokens), len(s2_tokens)))
        avg_len_log = np.log(0.1 + avg_len)
        self.cmp_order = QGram(int(1+avg_len_log))
        
        num_tokens = abs(len(s1_tokens) - len(s2_tokens))
        avg_len_tokens = abs(np.mean([len(x) for x in s1_tokens]) - np.mean([len(x) for x in s2_tokens]))
        cosine = self.cmp.distance(s1, s2)
        
        all_tokens = set(s1_tokens) | set(s2_tokens)
        
        chars = string.printable
        limit = len(chars)
        few_tokens = list(all_tokens)[:limit]
        
        token_map = {k:v for k, v in zip(few_tokens, chars)}
        mapped_s1 = "".join(token_map[x] for x in s1_tokens if x in token_map)
        mapped_s2 = "".join(token_map[x] for x in s2_tokens if x in token_map)
        
        order_dist = self.cmp_order.distance(mapped_s1, mapped_s2)
        # print((num_tokens / avg_len) * 20 , (avg_len_tokens / avg_len_log) * 10, cosine * 10, (order_dist / len(s1_tokens))*10)
            
        return (num_tokens / avg_len) * 20 + (avg_len_tokens / avg_len_log) * 10 + cosine * 10 + (order_dist / len(s1_tokens))*10
      
if __name__ == "__main__":
    cmp = MyMetric()
    dist = cmp.distance('my name is Peter Parker', 'Parker Peter name my is')

    if dist < 20:
        print('Likely similar')
