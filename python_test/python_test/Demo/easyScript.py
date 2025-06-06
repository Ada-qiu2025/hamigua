class Solution():
    def twoSum(self,nums,target):
        for i in range(len(nums)):
            f=nums(i)+nums(i+1)
            if target==f:
                return f
            else:
                pass

Solution.twoSum(self,[1,2,4,5],9)



class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return None

# 测试代码
solution = Solution()
print(solution.twoSum([1, 2, 4, 5], 9))  # 输出应为 [1, 3] 因为 nums[1] + nums[3] = 2 + 5 = 7

