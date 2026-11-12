class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        # Dictionary mapping each closing bracket to its corresponding opening bracket
        mapping = {")": "(", "}": "{", "]": "["}
        
        for char in s:
            # If the character is a closing bracket
            if char in mapping:
                # Pop the top element from the stack if it's non-empty; otherwise assign a dummy value
                top_element = stack.pop() if stack else '#'
                
                # If the popped element doesn't match the expected opening bracket, return False
                if mapping[char] != top_element:
                    return False
            else:
                # If it's an opening bracket, push it onto the stack
                stack.append(char)
                
        # If the stack is empty, all brackets were properly opened and closed
        return not stack