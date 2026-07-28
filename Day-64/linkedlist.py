class Node:
    """Represents a single node in a linked list."""

    def __init__(self, value):
        """
        Initializes a node with the given value.

        Args:
            value: Data to be stored in the node.
        """
        self.data = value
        self.next = None


class LinkedList:
    """Represents a singly linked list."""

    def __init__(self):
        """Initializes an empty linked list."""

        # Points to the first node
        self.head = None

        # Stores the number of nodes
        self.n = 0

    def __len__(self):
        """Returns the number of nodes in the linked list."""

        return self.n

    def insert_head(self, value):
        """
        Inserts a new node at the beginning of the linked list.

        Args:
            value: Value to be inserted.
        """

        # Create a new node
        new_node = Node(value)

        # Make the new node point to the current head
        new_node.next = self.head

        # Update head
        self.head = new_node

        # Increase list size
        self.n += 1

    def traverse(self):
        """Displays all elements of the linked list."""

        curr = self.head

        while curr is not None:
            print(curr.data, end=" ")
            curr = curr.next

        print()

    def __str__(self):
        """Returns the linked list as a formatted string."""

        curr = self.head
        result = ""

        while curr is not None:
            result += f"{curr.data}->"
            curr = curr.next

        return result[:-2]

    def append(self, value):
        """
        Inserts a new node at the end of the linked list.

        Args:
            value: Value to be appended.
        """

        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.n += 1
            return

        curr = self.head

        while curr.next is not None:
            curr = curr.next

        curr.next = new_node
        self.n += 1

    def insert_middle(self, after, value):
        """
        Inserts a new node after the specified value.

        Args:
            after: Existing node value.
            value: Value to insert.

        Raises:
            ValueError: If the target value is not found.
        """

        new_node = Node(value)
        curr = self.head

        while curr is not None:

            if curr.data == after:
                new_node.next = curr.next
                curr.next = new_node
                self.n += 1
                return

            curr = curr.next

        raise ValueError("Element not found")

    def search(self, value):
        """
        Searches for a value in the linked list.

        Returns:
            str: Search result.
        """

        curr = self.head

        while curr is not None:

            if curr.data == value:
                return "Found"

            curr = curr.next

        return "Item not found"

    def index(self, key):
        """
        Returns the element present at the given index.

        Args:
            key: Index position.

        Raises:
            IndexError: If the index is invalid.
        """

        if self.head is None:
            return "Empty LinkedList"

        curr = self.head
        pos = 0

        while curr is not None:

            if pos == key:
                return curr.data

            curr = curr.next
            pos += 1

        raise IndexError("Index out of range")
    def __delitem__(self, key):
        """
        Deletes the node at the specified index.

        Args:
            key: Index of the node to delete.

        Raises:
            IndexError: If the index is out of range.
        """

        if self.head is None:
            raise IndexError("Index out of range")

        # Delete the head node
        if key == 0:
            self.head = self.head.next
            self.n -= 1
            return

        curr = self.head
        pos = 0

        while curr.next is not None:

            if pos == key - 1:
                curr.next = curr.next.next
                self.n -= 1
                return

            curr = curr.next
            pos += 1

        raise IndexError("Index out of range")

    def popleft(self):
        """
        Removes the first node from the linked list.

        Raises:
            IndexError: If the linked list is empty.
        """

        if self.head is None:
            raise IndexError("Index out of range")

        self.head = self.head.next
        self.n -= 1

    def pop(self):
        """
        Removes the last node from the linked list.

        Raises:
            IndexError: If the linked list is empty.
        """

        if self.head is None:
            raise IndexError("Index out of range")

        # Handle single-node linked list
        if self.head.next is None:
            self.popleft()
            return

        curr = self.head

        while curr.next.next is not None:
            curr = curr.next

        curr.next = None
        self.n -= 1

    def remove(self, value):
        """
        Removes the first occurrence of the specified value.

        Args:
            value: Value to remove.

        Raises:
            ValueError: If the linked list is empty.
        """

        if self.head is None:
            raise ValueError("Element not found")

        # Remove head node
        if self.head.data == value:
            self.popleft()
            return

        curr = self.head

        while curr.next is not None:

            if curr.next.data == value:
                break

            curr = curr.next

        if curr.next is None:
            return "Item not found"

        curr.next = curr.next.next
        self.n -= 1

    def replace_max(self, value):
        """
        Replaces the maximum element in the linked list
        with the given value.

        Args:
            value: New value that replaces the maximum element.
        """

        max_value = float("-inf")
        curr = self.head

        while curr is not None:

            if curr.data > max_value:
                max_value = curr.data

            curr = curr.next

        self.insert_middle(max_value, value)
        self.remove(max_value)

    def odd_sum(self):
        """
        Calculates the sum of elements present at odd indices.

        Returns:
            int: Sum of elements at odd positions.
        """

        if self.head is None:
            return "There are no items in the linked list."

        curr = self.head
        pos = 0
        total = 0

        while curr is not None:

            if pos % 2 != 0:
                total += curr.data

            curr = curr.next
            pos += 1

        return total
    def reverse(self):
        """
        Reverses the linked list in-place.

        This method changes the direction of all node links,
        making the last node the new head.
        """

        # Previous node initially points to nothing
        prev_node = None

        # Start from the head node
        curr_node = self.head

        while curr_node is not None:

            # Store the next node
            next_node = curr_node.next

            # Reverse the current link
            curr_node.next = prev_node

            # Move previous and current pointers forward
            prev_node = curr_node
            curr_node = next_node

        # Update the head to the new first node
        self.head = prev_node

    def change_sent(self):
        """
        Replaces special characters with spaces.

        If two consecutive special characters are found,
        the following word is capitalized and the extra
        special character is removed.
        """

        curr = self.head

        while curr is not None:

            if not curr.data.isalnum():

                # Replace special character with a space
                curr.data = " "

                if not curr.next.data.isalnum():

                    # Capitalize the next word
                    curr.next.next.data = curr.next.next.data.title()

                    # Remove the extra special character
                    curr.next = curr.next.next

            curr = curr.next

    def remove_duplicates(self):
        """
        Removes duplicate values from the linked list.

        Only the first occurrence of each value is retained.
        """

        prev = None
        curr = self.head

        # Store visited values
        visited = set()

        while curr is not None:

            if curr.data in visited:

                # Skip duplicate node
                prev.next = curr.next
                self.n -= 1
                curr = curr.next

            else:

                visited.add(curr.data)
                prev = curr
                curr = curr.next

if __name__ == "__main__":
    ll = LinkedList()

    print("\n1. Testing append()")
    ll.append(10)
    ll.append(20)
    ll.append(30)
    ll.append(20)
    ll.append(40)
    ll.traverse()

    print("\n2. Testing insert_head()")
    ll.insert_head(5)
    print(ll)

    print("\n3. Testing __len__()")
    print(len(ll))

    print("\n4. Testing insert_middle()")
    ll.insert_middle(20, 25)
    print(ll)

    print("\n5. Testing search()")
    print(ll.search(25))
    print(ll.search(100))

    print("\n6. Testing index()")
    print(ll.index(0))
    print(ll.index(3))

    print("\n7. Testing remove()")
    ll.remove(20)
    print(ll)

    print("\n8. Testing __delitem__()")
    del ll[2]
    print(ll)

    print("\n9. Testing popleft()")
    ll.popleft()
    print(ll)

    print("\n10. Testing pop()")
    ll.pop()
    print(ll)

    print("\n11. Testing replace_max()")
    ll.replace_max(99)
    print(ll)

    print("\n12. Testing odd_sum()")
    print(ll.odd_sum())

    print("\n13. Testing reverse()")
    ll.reverse()
    print(ll)

    print("\n14. Testing remove_duplicates()")
    ll.append(25)
    ll.append(99)
    ll.append(25)
    ll.append(99)
    print("Before:")
    print(ll)

    ll.remove_duplicates()

    print("After:")
    print(ll)

    print("\n15. Testing change_sent()")

    sentence = LinkedList()

    words = "The * / moon * is * / blue".split()

    for word in words:
        sentence.append(word)

    print("Before:")
    sentence.traverse()

    sentence.change_sent()

    print("After:")
    sentence.traverse()

    print("\nAll tests completed successfully!")