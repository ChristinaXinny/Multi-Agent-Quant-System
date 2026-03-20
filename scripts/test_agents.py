"""Agent流程测试脚本"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.coordinator import CoordinatorAgent
from src.utils.logger import logger
from src.utils.config_loader import ConfigLoader


def main():
    """主函数"""
    logger.info("开始测试Agent流程...")

    # 加载配置
    config = ConfigLoader()

    # 创建协调器
    coordinator = CoordinatorAgent(config.config)

    # 测试股票代码
    test_ticker = "AAPL"

    logger.info(f"测试股票: {test_ticker}")

    try:
        # 运行完整流程
        result = coordinator.run(test_ticker)

        # 打印结果
        logger.info("=" * 50)
        logger.info("测试结果:")
        logger.info(f"股票: {result['ticker']}")
        logger.info(f"当前价格: ${result['current_price']:.2f}")

        if 'technical_analysis' in result:
            tech = result['technical_analysis']
            logger.info(f"LSTM预测: {tech.get('lstm_prediction', 'N/A')}")
            logger.info(f"RSI: {tech.get('rsi', 'N/A')}")

        if 'sentiment_analysis' in result:
            sent = result['sentiment_analysis']
            logger.info(f"情感得分: {sent.get('recent_sentiment', 'N/A')}")

        if 'recommendation' in result:
            rec = result['recommendation']
            logger.info(f"操作建议: {rec.get('action', 'N/A')}")
            logger.info(f"信心指数: {rec.get('confidence', 'N/A')}")
            logger.info(f"理由: {rec.get('reason', 'N/A')}")

        logger.info("=" * 50)
        logger.info("测试完成!")

    except Exception as e:
        logger.error(f"测试失败: {e}")
        raise


if __name__ == "__main__":
    main()
