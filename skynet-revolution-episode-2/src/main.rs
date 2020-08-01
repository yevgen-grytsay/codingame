use std::collections::{HashSet, VecDeque};
use std::io;
use std::collections::hash_set::Iter;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let inputs = input_line.split(" ").collect::<Vec<_>>();
    let n = parse_input!(inputs[0], i32); // the total number of nodes in the level, including the gateways
    let l = parse_input!(inputs[1], i32); // the number of links
    let e = parse_input!(inputs[2], i32); // the number of exit gateways

    let mut graph: Vec<HashSet<i32>> = (0..n).into_iter()
        .map(|_| -> HashSet<i32> {HashSet::new()})
        .collect();
    // let mut vertices:Vec<HashSet<i32>> = Vec::with_capacity(n as usize);
    let mut exit_list: Vec<i32> = Vec::new();


    for i in 0..l as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let n1 = parse_input!(inputs[0], i32); // N1 and N2 defines a link between these nodes
        let n2 = parse_input!(inputs[1], i32);
        // let n1u: usize = n1;
        graph[n1 as usize].insert(n2);
        graph[n2 as usize].insert(n1);
    }
    for i in 0..e as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let ei = parse_input!(input_line, i32); // the index of a gateway node
        exit_list.push(ei);
    }

    // println!("{:?}", graph);
    // return ();

    let mut network = Network {
        graph: graph,
        exits: exit_list,
    };

    // game loop
    loop {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let si = parse_input!(input_line, i32); // The index of the node on which the Skynet agent is positioned this turn

        let edge = get_best_exit(&network, si);

        println!("{} {}", edge.0, edge.1);

        network.remove_edge(edge);
    }
}

struct Node {
    index: i32,
    distance_from_virus: i32,
    priority: i32,
}

impl Node {
    fn new(index: i32, network: &Network, paths: &Vec<i32>) -> Node {
        let path = get_path_for_node(paths, index);
        let distance_from_virus = path.len() as i32;
        let red_edges_count = network.get_red_edges_count_for_path(&path);

        Node {
            index,
            distance_from_virus,
            priority: red_edges_count - path.len() as i32,
        }
    }
}

fn get_best_exit(network: &Network, si: i32) -> (i32, i32) {
    let mut nodes = network.create_nodes(si);

    nodes.sort_by(|a, b| {
        if a.priority != b.priority {
            return b.priority.cmp(&a.priority);
        }

        return a.distance_from_virus.cmp(&b.distance_from_virus);
    });

    let most_prioritized_hub = nodes[0].index;
    let exit: i32 = network.get_exits_for_node(most_prioritized_hub)[0];

    (most_prioritized_hub, exit)
}


struct Network {
    graph: Vec<HashSet<i32>>,
    exits: Vec<i32>,
}

impl Network {
    fn remove_edge(&mut self, edge: (i32, i32)) {
        self.graph[edge.0 as usize].remove(&edge.1);
        self.graph[edge.1 as usize].remove(&edge.0);
    }

    fn get_red_edges_count_for_path(&self, path: &Vec<i32>) -> i32 {
        let mut count = 0;

        for &node in path {
            count += self.get_red_edges_count_for_node(node);
        }

        count
    }

    fn get_red_edges_count_for_node(&self, node: i32) ->i32 {
        self.iter_neighbors(node)
            .filter(|n| {
                self.exits.contains(n)
            })
            .count() as i32
    }

    fn iter_neighbors(&self, node: i32) -> Iter<i32> {
        self.graph[node as usize].iter()
    }

    fn get_exits_for_node(&self, node: i32) -> Vec<i32> {
        self.iter_neighbors(node)
            .filter(|n| {
                self.exits.contains(n)
            })
            .cloned()
            .collect()
    }

    fn create_nodes(&self, si: i32) -> Vec<Node> {
        let mut visited: HashSet<i32> = HashSet::new();
        let mut paths: Vec<i32> = vec![-1; self.graph.len()];
        let mut queue: VecDeque<i32> = VecDeque::new();

        let mut nodes: Vec<Node> = Vec::new();

        queue.push_back(si);

        while !queue.is_empty() {

            let current = queue.pop_front().unwrap();
            visited.insert(current);

            if self.is_not_exit(current) {
                if self.get_red_edges_count_for_node(current) > 0 {
                    nodes.push(Node::new(current, &self, &paths));
                }
            }

            for &neighbor in self.iter_neighbors(current) {
                if self.is_exit(neighbor) {
                    continue;
                }

                if !visited.contains(&neighbor) {
                    paths[neighbor as usize] = current;
                    queue.push_back(neighbor);
                    visited.insert(neighbor);
                }
            }
        }

        nodes
    }

    fn is_exit(&self, node: i32) -> bool {
        self.exits.contains(&node)
    }

    fn is_not_exit(&self, node: i32) -> bool {
        !self.is_exit(node)
    }
}

fn get_path_for_node(parents: &Vec<i32>, node: i32) -> Vec<i32> {
    let mut path: Vec<i32> = Vec::new();
    let mut current = node;
    path.push(node);

    loop {
        let parent = parents[current as usize];
        if parent == -1 {
            break;
        }
        path.push(parent);
        current = parent;
    }

    path
}

#[cfg(test)]
mod tests {
    use super::*;

    mod parent_to_path {
        use super::*;

        #[test]
        fn test_single_node() {
            let parents = vec![-1, 0, 1];

            let path = get_path_for_node(&parents,0);

            assert_eq!(path, vec![0]);
        }

        #[test]
        fn test_three_nodes() {
            let parents = vec![-1, 0, 1];

            let path = get_path_for_node(&parents, 2);

            assert_eq!(path, vec![2, 1, 0]);
        }
    }
}
