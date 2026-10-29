class TreeNode:
    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None

    def __str__(self) -> str:
        result = ''
        if self.left:
            result += f', left:{self.left.key}'
        if self.right:
            result += f', right:{self.right.key}'
        return f'Node({self.key}{result})'


class BinarySearchTree:
    def __init__(self, root: TreeNode | None = None) -> None:
        self.root = root

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = TreeNode(key)
            return

        curr = self.root
        while True:
            if key < curr.key:
                if curr.left is None:
                    curr.left = TreeNode(key)
                    return
                curr = curr.left
            elif key > curr.key:
                if curr.right is None:
                    curr.right = TreeNode(key)
                    return
                curr = curr.right
            else:
                return

    @classmethod
    def build_from_preorder_keys(cls, keys: list[int]) -> 'BinarySearchTree':
        if not keys:
            return BinarySearchTree()

        root = TreeNode(keys[0])
        tree_stack = [root]

        for key in keys[1:]:
            if key < tree_stack[-1].key:
                node = TreeNode(key)
                tree_stack[-1].left = node
                tree_stack.append(node)
            else:
                last = tree_stack.pop()
                while tree_stack and tree_stack[-1].key < key:
                    last = tree_stack.pop()
                node = TreeNode(key)
                last.right = node
                tree_stack.append(node)
        return BinarySearchTree(root)

    def get_preorder(self) -> list[int]:
        res = []
        tree_stack = []
        curr = self.root

        while curr is not None or tree_stack:
            if curr is not None:
                res.append(curr.key)
                tree_stack.append(curr)
                curr = curr.left
            else:
                curr = tree_stack.pop()
                curr = curr.right

        return res

    def get_inorder(self) -> list[int]:
        res = []
        tree_stack = []
        curr = self.root

        while curr is not None or tree_stack:
            if curr is not None:
                tree_stack.append(curr)
                curr = curr.left
            else:
                curr = tree_stack.pop()
                res.append(curr.key)
                curr = curr.right

        return res

    def get_postorder(self) -> list[int]:
        res = []
        tree_stack = []
        curr = self.root
        last_visited = None

        while curr is not None or tree_stack:
            if curr is not None:
                tree_stack.append(curr)
                curr = curr.left
            else:
                peek_node = tree_stack[-1]
                if peek_node.right is not None and last_visited != peek_node.right:
                    curr = peek_node.right
                else:
                    res.append(peek_node.key)
                    last_visited = tree_stack.pop()

        return res
