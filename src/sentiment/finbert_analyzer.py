"""FinBERT情感分析模块"""
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Union
from loguru import logger


class FinBertAnalyzer:
    """FinBERT情感分析器"""

    def __init__(self, model_name: str = "ProsusAI/finbert"):
        """
        初始化FinBERT分析器

        Args:
            model_name: HuggingFace模型名称
        """
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1

        try:
            # 加载预训练模型和分词器
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

            # 创建pipeline
            self.classifier = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device
            )

            logger.info(f"FinBERT模型加载成功: {model_name}")

        except Exception as e:
            logger.error(f"FinBERT模型加载失败: {e}")
            raise

    def analyze_single(self, text: str) -> Dict[str, float]:
        """
        分析单条文本的情感

        Args:
            text: 输入文本

        Returns:
            情感得分字典
        """
        try:
            result = self.classifier(text)[0]

            # 将标签转换为得分 (-1到1)
            label_map = {
                'positive': 1,
                'negative': -1,
                'neutral': 0
            }

            label = result['label'].lower()
            score = result['score']

            # 计算综合情感得分
            sentiment_score = label_map.get(label, 0) * score

            return {
                'label': label,
                'confidence': score,
                'sentiment_score': sentiment_score
            }

        except Exception as e:
            logger.error(f"情感分析出错: {e}")
            return {
                'label': 'neutral',
                'confidence': 0.0,
                'sentiment_score': 0.0
            }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        批量分析文本情感

        Args:
            texts: 文本列表

        Returns:
            情感得分列表
        """
        results = []

        for text in texts:
            result = self.analyze_single(text)
            results.append(result)

        logger.info(f"批量情感分析完成,共 {len(texts)} 条")
        return results

    def analyze_news(
        self,
        news_df: 'pd.DataFrame',
        text_col: str = 'title'
    ) -> 'pd.DataFrame':
        """
        分析新闻数据情感

        Args:
            news_df: 新闻DataFrame
            text_col: 文本列名

        Returns:
            添加了情感列的DataFrame
        """
        import pandas as pd

        sentiments = []

        for text in news_df[text_col]:
            result = self.analyze_single(text)
            sentiments.append(result['sentiment_score'])

        news_df['sentiment_score'] = sentiments

        logger.info(f"新闻情感分析完成,平均得分: {np.mean(sentiments):.4f}")
        return news_df
