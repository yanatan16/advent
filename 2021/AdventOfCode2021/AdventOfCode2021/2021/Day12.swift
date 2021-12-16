//
//  Day12.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/13/21.
//

import Foundation


struct UnweightedUndirectedGraph {
    struct Node : Hashable, Equatable, CustomStringConvertible {
        let repr: String
        
        init(_ s: String) {
            repr = s
        }
        
        var description: String {
            repr
        }
        
        static func ==(l: Node, r: Node) -> Bool {
            l.repr == r.repr
        }
        
        var big : Bool {
            repr.uppercased() == repr
        }
    }
    
    typealias Edge = (Node, Node)
    typealias Path = [Node]
    
    let nodes: [Node]
    let edges: [Edge]
    
    init(edges: [Edge]) {
        nodes = Set(edges.flatMap { [$0.0, $0.1] }).map{$0}
        self.edges = edges
    }
    
    var adjacency : [Node:[Node]] {
        edges.reduce(into: [:]) { (adj, edge) in
            let (from, to) = edge
            adj[from, default:[]] += [to]
            adj[to, default:[]] += [from]
        }
    }
    
    func allPaths(start: Node, end: Node, validPath: (Path) -> Bool) -> [Path] {
        var finishedPaths:Set<Path> = Set()
        var unfinishedPaths:Set<Path> = Set([[start]])
        let adjacency = self.adjacency
        // var printer = IterationPrinter()
        
        while unfinishedPaths.count > 0 {
            // printer.iterprint("paths finished \(finishedPaths.count) unfinished \(unfinishedPaths.count)")
            let path = unfinishedPaths.popFirst()!
            let nextPaths = adjacency[path.last!, default: []].map { node in
                path + [node]
            }.filter(validPath)
            
            nextPaths.forEach { path in
                if path.last! == end {
                    finishedPaths.insert(path)
                } else {
                    unfinishedPaths.insert(path)
                }
            }
        }
        
        return finishedPaths.map{$0}
    }
}

// start: 7:14
// part 1: 7:37 (23m)
// part 2: 7:47 (33m)
struct Day12 : Solution {
    var exampleRawInput: String { """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""}
    
    typealias Input = UnweightedUndirectedGraph
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        UnweightedUndirectedGraph(
            edges: raw.splitlines().map { line in
                let split = line.components(separatedBy: "-")
                return (.init(split[0]), .init(split[1]))
            }
        )
    }
    
    
    func problem1(_ input: Input) -> Int {
        return input.allPaths(
            start: .init("start"),
            end: .init("end"),
            validPath: { path in
                // No two small nodes
                path.filter { node in
                    !node.big
                }.frequencies().values.filter { count in
                    count > 1
                }.count == 0
            }
        ).count
    }
    
    func problem2(_ input: Input) -> Int {
        let paths = input.allPaths(
            start: .init("start"),
            end: .init("end"),
            validPath: { path in
                // Only a single small node (non-start/end) can be visited twice
                let freqs = path.filter { node in
                    !node.big
                }.frequencies()
                if freqs[.init("start"), default:0] > 1 {
                    return false
                }
                if freqs.values.filter({ count in count > 1 }).count > 1 {
                    return false
                }
                if freqs.values.filter({ count in count > 2 }).count > 0 {
                    return false
                }
                return true
            }
        )
        
        return paths.count
    }
}
