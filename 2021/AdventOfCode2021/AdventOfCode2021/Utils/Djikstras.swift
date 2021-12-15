//
//  Djikstras.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/15/21.
//

import Foundation

func djisktrasPathFind<Node>(
    nodes: Set<Node>,
    start: Node,
    startingDistances: [Node:Int],
    neighbors: (Node) -> [Node],
    weight: (Node) -> Int
) -> [Node:Int] {
    var unvisitedSet = nodes
    var current = start
    var distance = startingDistances
    
    var printer = IterationPrinter()
    
    while unvisitedSet.count > 0 {
        printer.iterprint("unvisited set size \(unvisitedSet.count)")
        
        let currentDistance = distance[current]!
        let unvisitedNeighbors = neighbors(current).filter { n in
            unvisitedSet.contains(n)
        }
        unvisitedNeighbors.forEach { n in
            let tentativeDistance = currentDistance + weight(n)
            distance[n] = min(tentativeDistance, distance[n, default: Int.max])
        }
        unvisitedSet.remove(current)
        
        if let newCurrent = unvisitedSet.min(by: { (l, r) in
            distance[l, default: Int.max] <= distance[r, default: Int.max]
        }) {
            current = newCurrent
        }
    }
    
    return distance
}
