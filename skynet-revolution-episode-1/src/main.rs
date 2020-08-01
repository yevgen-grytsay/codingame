use std::io;
use std::collections::{HashSet, VecDeque};

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

    // game loop
    loop {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let si = parse_input!(input_line, i32); // The index of the node on which the Skynet agent is positioned this turn

        let paths = create_paths(&graph, si);
        let nearest_exit = if exit_list.len() == 1 {exit_list[0]} else {get_nearest_exit(&paths, &exit_list, si)};
        // Write an action using println!("message...");
        // To debug: eprintln!("Debug message...");


        // Example: 0 1 are the indices of the nodes you wish to sever the link between
        let node_to_cut = paths[nearest_exit as usize];
        println!("{} {}", nearest_exit, &node_to_cut);

        graph[nearest_exit as usize].remove(&node_to_cut);
        graph[node_to_cut as usize].remove(&nearest_exit);
    }
}

fn get_nearest_exit(paths: &Vec<i32>, exit_list: &Vec<i32>, si: i32) -> i32 {
    let mut min_len: i32 = paths.len() as i32;
    let mut nearest_exit: Option<i32> = None;

    for &exit in exit_list {
        let current_len = get_path_length(paths, exit, si);
        if current_len > -1 && current_len < min_len {
            min_len = current_len;
            nearest_exit.replace(exit);
        }
    }

    nearest_exit.unwrap()
}

fn get_path_length(paths: &Vec<i32>, exit: i32, si: i32) -> i32 {
    let mut length = 0;
    let mut current = exit;
    loop {
        let parent = paths[current as usize];

        if parent == -1 {
            return -1;
            // panic!("Can not get path length (either path does not exists or nodes are passed to the function in reverse order)");
        }

        current = parent;
        length += 1;

        if parent == si {
            break;
        }
    }

    length
}

fn create_paths(graph: &Vec<HashSet<i32>>, si: i32) -> Vec<i32> {
    let mut visited: HashSet<i32> = HashSet::new();
    let mut paths: Vec<i32> = vec![-1; graph.len()];
    let mut queue: VecDeque<i32> = VecDeque::new();


    queue.push_back(si);

    while !queue.is_empty() {

        let mut current = queue.pop_front().unwrap();

        visited.insert(current);

        for &neighbor in graph[current as usize].iter() {
            if !visited.contains(&neighbor) {
                paths[neighbor as usize] = current;
                queue.push_back(neighbor);
                visited.insert(neighbor);
            }
        }
    }

    paths
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_shortest_path() {
        let mut graph: Vec<HashSet<i32>> = vec![
            vec![1, 2].into_iter().collect(),
            vec![0, 3].into_iter().collect(),
            vec![0, 3].into_iter().collect(),
            vec![1, 2].into_iter().collect(),
        ];

        let paths = create_paths(&graph, 0);
        assert_eq!(paths.len(), 4);
        assert_eq!(paths[0], -1);
        assert_eq!(paths[1], 0);
        assert_eq!(paths[2], 0);
        assert!(paths[3] == 1 || paths[3] == 2);
    }

    #[test]
    fn test_get_path_length() {
        let paths: Vec<i32> = vec![-1, 0, 0, 2];

        let len = get_path_length(&paths, 3, 0);

        assert_eq!(len, 2);
    }

    #[test]
    fn test_find_nearest_exit() {
        let paths: Vec<i32> = vec![-1, 0, 0, 2];
        let exit_list: Vec<i32> = vec![3, 2];

        let nearest = get_nearest_exit(&paths, &exit_list, 0);

        assert_eq!(nearest, 2);
    }
}
