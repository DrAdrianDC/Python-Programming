class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
       
       ## Sorting
       intervals.sort(key=lambda x: x[0])  
       ## Merge intervals
       merged = [intervals[0]]
       for current in intervals[1:]:
        last_merged = merged[-1]
        if last_merged[1] >= current[0]:
           last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
       return merged