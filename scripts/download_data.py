"""数据下载脚本"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.data_fetcher import DataFetcher
from src.utils.logger import logger
from src.utils.config_loader import ConfigLoader


def main():
    """主函数"""
    logger.info("开始下载数据...")

    # 加载配置
    config = ConfigLoader()
    tickers = config.get_stocks()
    stocks_config = config.get('stocks', {})

    start_date = stocks_config.get('start_date', '2020-01-01')
    end_date = stocks_config.get('end_date', '2025-12-31')

    logger.info(f"股票列表: {tickers}")
    logger.info(f"日期范围: {start_date} 到 {end_date}")

    # 创建数据获取器
    fetcher = DataFetcher()

    # 批量下载
    results = fetcher.fetch_multiple_stocks(tickers, start_date, end_date)

    logger.info(f"数据下载完成!成功下载 {len(results)} 只股票")

    # 创建示例新闻数据
    from src.data.news_loader import NewsLoader
    news_loader = NewsLoader()
    news_loader.create_sample_news()

    logger.info("示例新闻数据已创建")


if __name__ == "__main__":
    main()
