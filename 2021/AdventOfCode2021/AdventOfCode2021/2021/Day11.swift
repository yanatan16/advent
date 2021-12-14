//
//  Day11.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/13/21.
//

import Foundation


// start: 1:40
// part 1: 2:11 (31m)
// part 2: 2:15 (35m)
struct Day11 : Solution {
    var exampleRawInput: String { """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""}
    
    typealias Input = [[Int]]
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().map { $0.compactMap { Int(String($0)) }}
    }
    
    struct State {
        let octopi : Input
        let flashCount : Int
        let iteration : Int
        
        func step() -> State {
            // print("Start Step \(iteration+1) [\(flashCount)] \(octopi)")
            var stepOctopi = octopi.map { $0.map { o in o + 1} }
            var newFlashes: Set<TwoDIndex> = Set()
            var stepFlashes:Set<TwoDIndex> = Set()
            var first = true
            
            while first || newFlashes.count > 0 {
                first = false
                
                newFlashes.forEach { idx in
                    idx.allNeighbors().forEach { nidx in
                        stepOctopi.safe2DUpdate(nidx) { $0 + 1 }
                    }
                }
                
                stepFlashes = stepFlashes.union(newFlashes)
                newFlashes = Set()
                
                stepOctopi.twoDIndices().forEach { idx in
                    if stepOctopi.safe2DGet(idx)! > 9 && !stepFlashes.contains(idx) {
                        newFlashes.insert(idx)
                    }
                }
            }
            
            stepFlashes.forEach { idx in
                stepOctopi.safe2DUpdate(idx) { _ in 0 }
            }
            

            // print("Found \(stepFlashes.count) new Flashes \(stepFlashes)")
            
            return State(octopi: stepOctopi, flashCount: flashCount + stepFlashes.count,
                         iteration: iteration + 1)
        }
    }
    
    func problem1(_ input: Input) -> Int {
        (1...100).reduce(State(octopi: input, flashCount: 0, iteration: 0)) { (state, _) in
            state.step()
        }.flashCount
    }
    
    func problem2(_ input: Input) -> Int {
        var state = State(octopi: input, flashCount: 0, iteration: 0)
        let target = input.twoDIndices().count
        while true {
            let next = state.step()
            if next.flashCount - state.flashCount == target {
                return next.iteration
            }
            state = next
        }
    }
}
