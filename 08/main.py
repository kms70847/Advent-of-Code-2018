def get_tree(stack):
    num_children = stack.pop()
    num_metadata = stack.pop()
    result = {"children": [], "metadata": []}
    for _ in range(num_children):
        result["children"].append(get_tree(stack))
    for _ in range(num_metadata):
        result["metadata"].append(stack.pop())
    return result

def metadata_sum(t):
    return sum(t["metadata"]) + sum(metadata_sum(child) for child in t["children"])

def value(t):
    if not t["children"]:
        return sum(t["metadata"])
    return sum(value(t["children"][m-1]) for m in t["metadata"] if m > 0 and m < len(t["children"])+1)

with open("input") as file:
    data = [int(x) for x in file.read().split()]

data.reverse()
t = get_tree(data)
print(metadata_sum(t))
print(value(t))