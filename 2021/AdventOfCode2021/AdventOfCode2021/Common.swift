//
//  Common.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

protocol Solution {
    var exampleRawInput:String {get}
    associatedtype Input
    associatedtype Output
    func parseInput(_ raw: String) -> Input
    func problem1(_ input: Input) -> Output
    func problem2(_ input: Input) -> Output
}

extension Solution {
    func run(_ raw: String) {
        let example = parseInput(exampleRawInput)
        
        print("Example Problem 1: \(solve(example, problem1))")
        print("Example Problem 2: \(solve(example, problem2))")
        
        let input = parseInput(raw)
        
        print("Solving Problem 1: \(solve(input, problem1))")
        print("Solving Problem 2: \(solve(input, problem2))")
    }
}

extension String {
    public func splitlines() -> [String] {
        self.components(separatedBy: "\n")
    }
    public func split2lines() -> [String] {
        self.components(separatedBy: "\n\n")
    }
}

public func solve<I,O>(_ input: I, _ solver: (I) -> O) -> String {
    let start = Date.now
    let out = solver(input)
    let time = Date.now.timeIntervalSince(start)
    return "\(out) \(floor(time*1000))ms"
}
