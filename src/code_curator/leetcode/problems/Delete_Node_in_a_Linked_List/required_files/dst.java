class Solution
{
    public ListNode deleteNode(ListNode node)
    {
        node.val = node.next.val;
        node.next = node.next.next;
    }

    public String some_func_with_name(int number)
    {
        System.out.println("Hello, World!");
    }
}