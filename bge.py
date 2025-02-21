# 和bge模型有关的代码都在这里

from FlagEmbedding import FlagModel

# 初始化模型
model = FlagModel('BAAI/bge-small-zh-v1.5', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)  # 使用fp16加速计算，但会稍微降低性能

# 计算相似度
def compute_similarity(sentences_1, sentences_2):
    """
    计算两个文本集合的相似度。
    
    输入：
    - sentences_1: 第一个文本集合，列表形式
    - sentences_2: 第二个文本集合，列表形式
    
    输出：
    - similarity: 两个文本集合之间的相似度矩阵
    """
    # 转换文本为向量
    embeddings_1 = convert_to_vector(sentences_1)
    embeddings_2 = convert_to_vector(sentences_2)
    
    # 计算相似度
    similarity = embeddings_1 @ embeddings_2.T
    return similarity

# 将文本转化为向量
def convert_to_vector(sentences):
    """
    将中文文本转化为向量。
    
    输入：
    - sentences: 需要转化的中文文本，列表形式
    
    输出：
    - embeddings: 文本对应的向量表示
    """
    embeddings = model.encode(sentences)
    return embeddings

# 示例用法
if __name__ == "__main__":
    sentences_1 = ["奶酪", "芝士"]
    sentences_2 = ["我爱吃奶酪", "今天去吃奶酪火锅吧？"]
    
    # 计算相似度
    similarity = compute_similarity(sentences_1, sentences_2)
    print(f"相似度矩阵：\n{similarity}")

    # 查询与文档的相似度
    queries = ['奶酪']
    passages = ["想吃奶酪"]
    q_embeddings = convert_to_vector(queries)
    p_embeddings = convert_to_vector(passages)
    scores = q_embeddings @ p_embeddings.T
    print(f"查询与文档的相似度分数：\n{scores}")