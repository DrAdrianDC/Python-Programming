class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if not prices:
            return 0
        
        min_price = prices[0]
        max_profit = 0
        
        for price in prices[1:]:
            # Update the minimum price if we find a lower one
            if price < min_price:
                min_price = price
            # If we sell today, calculate the profit and update the maximum if it's higher
            elif price - min_price > max_profit:
                max_profit = price - min_price
                
        # Return the maximum profit found after checking all prices
        return max_profit 