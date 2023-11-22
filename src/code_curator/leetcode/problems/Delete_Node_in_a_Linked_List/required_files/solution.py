class Solution:
    def deleteNode(node: ListNode) -> None:
        node.val = node.next.val
        node.next = node.next.next