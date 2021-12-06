//
//  Day2.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day2 : Solution {
    var exampleRawInput: String { """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""}
    
    enum Instruction {
        case forward(x:Int)
        case down(x:Int)
        case up(x:Int)
    }
    
    typealias Input = [Instruction]
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().compactMap { s in
            let ss : [Substring] = s.description.split(whereSeparator: \.isWhitespace)
            if ss.count != 2 {
                return nil
            }
            
            let x = Int(ss[1])!
            switch ss[0] {
            case "forward":
                return .forward(x: x)
            case "up":
                return .up(x:x)
            case "down":
                return .down(x:x)
            default:
                return nil
            }
        }
    }
    
    
    func plotHoriz(path : [Instruction]) -> Int {
        path.map { inst in
            switch inst {
            case .forward(let x):
                return x
            default:
                return 0
            }
        }.reduce(0) { $0 + $1 }
    }

    func plotVert(path : [Instruction]) -> Int {
        path.map { inst in
            switch inst {
            case .up(let x):
                return -x
            case .down(let x):
                return x
            default:
                return 0
            }
        }.reduce(0) { $0 + $1 }
    }

    
    func problem1(_ input: Input) -> Int {
        plotHoriz(path: input) * plotVert(path: input)
    }
    
    struct SubmarineDepthState {
        let aim : Int
        let depth : Int
    }
    
    func plotVertUsingAim(path : [Instruction]) -> Int {
        path.reduce(SubmarineDepthState(aim: 0, depth: 0)) { (state, inst) in
            switch inst {
            case .forward(let x):
                return SubmarineDepthState(aim:state.aim, depth: state.depth + state.aim * x)
            case .up(let x):
                return SubmarineDepthState(aim: state.aim - x, depth: state.depth)
            case .down(let x):
                return SubmarineDepthState(aim: state.aim + x, depth: state.depth)
            }
        }.depth
    }

    
    func problem2(_ input: Input) -> Int {
        // Horizontal is the same in problem 2
        plotHoriz(path: input) * plotVertUsingAim(path: input)
    }
}
