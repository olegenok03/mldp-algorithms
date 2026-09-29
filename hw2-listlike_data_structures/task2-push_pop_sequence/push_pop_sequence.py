def validate_push_pop_sequence(pushed: list[int], popped: list[int]) -> bool:
    stack = []
    i, j = 0, 0
    n = len(pushed)
    while i < n or j < n:
        if stack and stack[-1] == popped[j]:
            stack.pop()
            j += 1
        elif i < n:
            stack.append(pushed[i])
            i += 1
        else:
            return False
    return True


if __name__ == '__main__':
    pushed = [int(x) for x in input().split()]
    popped = [int(x) for x in input().split()]
    result = validate_push_pop_sequence(pushed, popped)
    print(result)
