import networkx as nx
import matplotlib.pyplot as plt
from lxml import etree
from urllib.parse import urlparse
import pydot

def parse_sitemap(file_path):
    tree = etree.parse(file_path)
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = tree.xpath('//ns:url/ns:loc/text()', namespaces=ns)
    return urls

'''def build_tree(urls):
    G = nx.DiGraph()
    G.add_node('root', label='root')

    blog_posts = count_blog_posts(urls)
    G.add_node('blog_posts', label=f'{blog_posts} blog posts')
    G.add_edge('root', 'blog_posts')

    for url in urls:
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        path = parsed_url.path.strip('/').split('/')
        parent = domain

        if parent not in G.nodes:
            G.add_node(parent, label=parent)
            G.add_edge('root', parent)

        if '/blog/' not in url:  # Skip blog posts
            for i, p in enumerate(path):
                node_name = '/'.join([parent] + path[:i+1])
                if node_name not in G.nodes:
                    G.add_node(node_name, label=p)
                G.add_edge(parent, node_name)
                parent = node_name

    return G
'''

def build_tree(urls):
    G = nx.DiGraph()
    G.add_node('root', label='root')

    '''blog_posts = count_blog_posts(urls)
    G.add_node('blog_posts', label=f'{blog_posts} blog posts')
    G.add_edge('root', 'blog_posts')'''

    for url in urls:
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        path = parsed_url.path.strip('/').split('/')
        parent = domain.replace('/', '_').replace(':', '_')  # Replace special characters with underscores

        if parent not in G.nodes:
            G.add_node(parent, label=parent)
            G.add_edge('root', parent)

        if '/blog/' not in url:  # Skip blog posts
            for i, p in enumerate(path):
                node_name = '/'.join([parent] + path[:i+1]).replace('/', '_').replace(':', '_')  # Replace special characters with underscores
                if node_name not in G.nodes:
                    G.add_node(node_name, label=p)
                G.add_edge(parent, node_name)
                parent = node_name

    return G
def visualize_tree(G):
    # Convert the NetworkX graph to a Pydot graph
    P = nx.drawing.nx_pydot.to_pydot(G)

    # Set the graph layout to 'dot'
    P.set_prog('dot')

    # Get the node positions from the Pydot graph
    pos = P.get_node_list()

    # Extract the positions from the Pydot nodes
    pos_dict = {}
    for node in pos:
        node_name = node.get_name().strip('"')
        pos_str = node.get_pos()
        if pos_str is not None:
            x, y = pos_str.strip('"').split(',')
            pos_dict[node_name] = (float(x), float(y))

    # Add a fallback position for the 'root' node if it doesn't have a position
    if 'root' not in pos_dict:
        pos_dict['root'] = (0, 0)

    plt.figure(figsize=(20, 20))
    labels = {n: G.nodes[n]['label'] for n in G.nodes}

    node_sizes = [3000 if G.nodes[n]['label'] == 'root' or '://' in G.nodes[n]['label'] else 1500 for n in G.nodes]

    nx.draw(G, pos_dict, labels=labels, with_labels=True, node_size=node_sizes, node_color="lightblue", arrows=True)
    plt.savefig('family_tree.png')
    plt.show()
'''def count_blog_posts(urls):
    count = 0
    for url in urls:
        if '/blog/' in url:
            count += 1
    return count'''

if __name__ == '__main__':
    file_path = 'sitemap.xml'  # Your sitemap.xml file path
    urls = parse_sitemap(file_path)
    tree = build_tree(urls)
    visualize_tree(tree)
