## 1. Two Sum

Python solution for LeetCode Problem 1: **Two Sum**.

## Approach

This solution uses a hash map (dictionary) to achieve an optimal **$O(n)$ time complexity**. 

Instead of using nested loops, it iterates through the array only once, checking if the complement (`target - current_number`) already exists in the dictionary. If it does, the indices are returned immediately; otherwise, the current number and its index are stored for future checks.
