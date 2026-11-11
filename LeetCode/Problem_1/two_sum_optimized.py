class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        index = {}
        for i in range(len(nums)):
            rest = target - nums[i]
            if rest in index:         
                return [index[rest],i]
            index[nums[i]] = i  