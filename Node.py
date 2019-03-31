class Node:
    """ This class in as abrastraction a search node


    :var state: Store the current state.
    :var cost: Store the path cost from the beginning until the actual node
    :var parent: Store a pointer to the parent node
    :var action: Store an action
    """
    def __init__(self, state, cost, parent=None, action=None):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        if self.parent:
            self.height = self.parent.height + 1
        else:
            self.height = 0


    def __repr__(self):
        return "<Node {}>".format(self.state)
		
		
def main():

	root_node = Node(('hello'), 0, parent=None, action=2)
	leaf_node = Node(('he','llo'), 1, parent=root_node, action=2)
	second_node = Node(('he','ll','o'), 3, parent=leaf_node, action=None)
	third_node = Node(('he', 'll', 'o'), 3, parent=second_node, action=None)
	
	cur_node = third_node
	path_cost = 0
	it = 0
	
	path = []
	while cur_node != root_node:
		path.append((cur_node, path_cost))
		path_cost+=cur_node.cost
		cur_node = cur_node.parent
		
	print(path)
	
if __name__ == '__main__':
    main()
