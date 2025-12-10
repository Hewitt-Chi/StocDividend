from dataclasses import dataclass


@dataclass
class InvestmentConfig:
    """投資設定參數"""
    stock_price: float = 53.5              # 股價
    monthly_dividend_per_share: float = 0.63  # 每股每月配息金額
    months_per_quarter: int = 3
    quarters_per_year: int = 4


class DividendCalculator:
    """QQQI 配息再投入計算器"""

    def __init__(self, config: InvestmentConfig | None = None):
        self.config = config or InvestmentConfig()
        self.total_shares = 0.0

    def calculate_dividend_shares(self) -> float:
        """計算當月配息可換得的股數"""
        dividend_amount = self.total_shares * self.config.monthly_dividend_per_share
        return dividend_amount / self.config.stock_price

    def simulate(self, years: int, shares_per_quarter: float, verbose: bool = False) -> dict:
        """模擬投資過程"""
        self.total_shares = 0.0
        total_quarters = years * self.config.quarters_per_year

        for quarter in range(1, total_quarters + 1):
            # 每季定期買入
            self.total_shares += shares_per_quarter

            if verbose:
                print(f"\n{'='*50}")
                print(f"第 {quarter} 季：買入 {shares_per_quarter} 股，目前持股：{self.total_shares:.4f}")

            # 每月配息再投入
            for month in range(1, self.config.months_per_quarter + 1):
                dividend_shares = self.calculate_dividend_shares()
                
                if verbose:
                    print(f"  第 {month} 月 | 配息前：{self.total_shares:.4f} 股 | 配息：+{dividend_shares:.4f} 股", end="")
                
                self.total_shares += dividend_shares  # 配息加入持股，影響下個月計算
                
                if verbose:
                    print(f" | 配息後：{self.total_shares:.4f} 股")

        return self._generate_summary(years, shares_per_quarter)

    def _generate_summary(self, years: int, shares_per_quarter: float) -> dict:
        """產生投資摘要"""
        total_invested = shares_per_quarter * years * self.config.quarters_per_year
        total_value = self.total_shares * self.config.stock_price
        monthly_dividend_shares = self.calculate_dividend_shares()
        monthly_dividend_value = monthly_dividend_shares * self.config.stock_price

        return {
            'years': years,
            'total_invested_shares': total_invested,
            'total_shares': self.total_shares,
            'total_value': total_value,
            'shares_from_dividend': self.total_shares - total_invested,
            'monthly_dividend_shares': monthly_dividend_shares,
            'monthly_dividend_value': monthly_dividend_value,
        }


def print_summary(summary: dict, config: InvestmentConfig) -> None:
    """格式化輸出投資摘要"""
    print(f"\n{'='*50}")
    print("📊 投資結果摘要")
    print(f"{'='*50}")
    print(f"投資期間：{summary['years']} 年")
    print(f"每股股價：${config.stock_price}")
    print(f"每股月配息：${config.monthly_dividend_per_share}")
    print(f"{'='*50}")
    print(f"總投入股數：{summary['total_invested_shares']:.2f} 股")
    print(f"配息累積股數：{summary['shares_from_dividend']:.4f} 股")
    print(f"最終總持股：{summary['total_shares']:.4f} 股")
    print(f"最終總市值：${summary['total_value']:,.2f}")
    print(f"{'='*50}")
    print("💰 未來每月被動收入（以最終持股計算）")
    print(f"每月配息股數：{summary['monthly_dividend_shares']:.4f} 股")
    print(f"每月配息金額：${summary['monthly_dividend_value']:.2f}")
    print(f"{'='*50}")


def get_user_input() -> tuple[int, float]:
    """取得使用者輸入"""
    while True:
        try:
            user_input = input("請輸入 [投資年數] [每季買入股數]：")
            years, shares = user_input.split()
            years, shares = int(years), float(shares)
            if years <= 0 or shares <= 0:
                raise ValueError("數值必須大於 0")
            return years, shares
        except ValueError as e:
            print(f"輸入錯誤：{e}")


def main():
    config = InvestmentConfig(
        stock_price=53.5,
        monthly_dividend_per_share=0.63  # 每股每月配息
    )

    calculator = DividendCalculator(config)
    years, shares_per_quarter = get_user_input()

    summary = calculator.simulate(years, shares_per_quarter, verbose=True)
    print_summary(summary, config)


if __name__ == "__main__":
    main()

# %%


# %%


# %%



