//
//  Day15.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/15/21.
//

import Foundation

// start 8:49
// part 1: 9:31
// part 2: 10:53
struct Day15 : Solution {
    var exampleRawInput: String { """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""}
    
    typealias Input = [[Int]]
    typealias Output = Int
    
    typealias Path = [TwoDIndex]
    typealias WeightedPath = (weight: Int, path: Path)
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().map { line in
            line.map { Int(String($0))! }
        }
    }
    
    func walkOneStep(_ input: Input, wp: WeightedPath) -> [WeightedPath] {
        wp.path.last!.squareNeighbors()
            .filter { neighbor in
                input.safe2DGet(neighbor) != nil &&
                !wp.path.contains(neighbor)
            }.map { neighbor in
                (weight: wp.weight + input.safe2DGet(neighbor)!,
                 path: wp.path + [neighbor])
            }
    }
    
    func minimizeWeightedPathFind(_ input: Input) -> WeightedPath {
        let start = TwoDIndex(0,0)
        let end = TwoDIndex(input.count-1, input[0].count-1)
        let initialWeight = 0
        var paths:SortedArray<WeightedPath> = .init { (lhs, rhs) in
            lhs.weight < rhs.weight
        }
        paths.insert((weight: initialWeight, path: [start]))
        
        while paths.first!.path.last! != end {
            let lowestWeightPath = paths.removeFirst()
            
            let nextPaths = walkOneStep(input, wp: lowestWeightPath)
            
            nextPaths.forEach { wp in
                paths.insert(wp)
            }
        }
        
        return paths.first!
    }
    
    func problem1(_ input: Input) -> Int {
        djisktrasPathFind(
            nodes: Set(input.twoDIndices()),
            start: TwoDIndex(0,0),
            startingDistances: [TwoDIndex(0,0): 0],
            neighbors: { idx in
                idx.squareNeighbors()
                    .filter { input.safe2DGet($0) != nil }
            },
            weight: { idx in input.safe2DGet(idx)! }
        )[TwoDIndex(input.count-1, input[0].count-1)]!
    }
    
    func problem2(_ input: Input) -> Int {
        let origRows = input.count
        let origCols = input[0].count
        let rows = origRows * 5
        let cols = origCols * 5
        
        let weight : (TwoDIndex) -> Int = { idx in
            let i5div = idx.i / origRows
            let i5rem = idx.i % origRows
            
            let j5div = idx.j / origCols
            let j5rem = idx.j % origCols
            
            let orig = input.safe2DGet(TwoDIndex(i5rem, j5rem))!
            let increased = orig + i5div + j5div
            
            if increased > 9 {
                return increased - 9
            } else {
                return increased
            }
        }
        
        var allDistances:[TwoDIndex:Int] = [:]
        
        for I in 0...4 {
            let nodes = (0...(origRows-1)).flatMap { i in
                (0...(cols-1)).map { j in
                    TwoDIndex(I*origRows + i, j)
                }
            }
            var startingDistances:[TwoDIndex:Int] = [:]
            if I > 0 {
                for j in 0...(cols-1) {
                    let bigIndex = TwoDIndex(I*origRows,j)
                    let edgeAbove = TwoDIndex(I*origRows-1,j)
                    
                    startingDistances[bigIndex] = allDistances[edgeAbove]! + weight(bigIndex)
                }
            } else {
                startingDistances[TwoDIndex(0,0)] = 0
            }
            
            print("Submap \(I) first[\(nodes.first!)]")
            print("starting \(startingDistances)")

            
            let submap = djisktrasPathFind(
                nodes: Set(nodes),
                start: TwoDIndex(I*origRows, 0),
                startingDistances: startingDistances,
                neighbors: { idx in
                    idx.squareNeighbors()
                        .filter { idx in
                            idx.i >= (I-1) * origRows && idx.i < ((I+1)*origRows) &&
                            idx.j >= 0 && idx.j < cols
                        }
                },
                weight: weight
            )
            
            submap.forEach { (node, dist) in
                allDistances[node] = dist
            }
        }
        
        return allDistances[TwoDIndex(rows-1,cols-1)]!
    }
}
