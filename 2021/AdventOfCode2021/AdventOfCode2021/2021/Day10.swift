//
//  Day10.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/13/21.
//

import Foundation

// start time: 4:48
// part 1: 5:10 22m
// part 2: 5:15 27m
struct Day10 : Solution {
    var exampleRawInput: String { """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""}
    
    typealias Line = String
    typealias Input = [Line]
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().filter { $0.count > 0 }
    }
    
    enum Chunk: Error {
        case corrupted(found: Character)
        case incomplete(expected: String)
        case end
    }
    
    func eval(_ s: String) throws -> [Character] {
        var open:[Character] = []
        var cs = s.map{$0}
        //print("evaluating \(s)")
        while !cs.isEmpty {
            let next = cs[0]
            cs = cs[1...].map{$0}
            
            if closers[next] != nil {
                //print("opener \(next)")
                open.append(next)
            } else if closers[open.last!] == next {
                open = open[...(open.count-2)].map{$0}
                //print("valid closer \(next) (openers: \(open))")
            } else {
                throw Chunk.corrupted(found: next)
            }
        }
        
        return open.reversed().map { opener in closers[opener]! }
    }
    
    let closers: [Character:Character] = [
        "(":")",
        "[":"]",
        "{":"}",
        "<":">"
    ]
    let scores:[Character:Int] = [
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    ]
    
    func problem1(_ input: Input) -> Int {
        input.compactMap { (l:Line)->Character? in
            do {
                try eval(l)
                return nil
            } catch Chunk.corrupted(let found) {
                //print("line \(l) corrupted with \(found)")
                return found
            } catch {
                return nil
            }
        }.map { (ch:Character) in
            scores[ch]!
        }.sum()
    }
    
    
    let scores2:[Character:Int] = [
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    ]
    
    func autocompleteScore(_ fix: [Character]) -> Int {
        fix.reduce(0) { (score, c) in
            score * 5 + scores2[c]!
        }
    }
    
    func problem2(_ input: Input) -> Int {
        input.compactMap { (l:Line)->[Character]? in
            do {
                return try eval(l)
            } catch Chunk.corrupted(_) {
                return nil
            } catch {
                return nil
            }
        }.map { (fix: [Character]) in
            autocompleteScore(fix)
        }.median()
    }
}
