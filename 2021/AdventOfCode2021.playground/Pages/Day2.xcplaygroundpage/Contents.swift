//: [Previous](@previous)

import Foundation

let fileURL = Bundle.main.url(forResource: "input", withExtension: "txt")
let rawInput = try! String(contentsOf: fileURL!, encoding: String.Encoding.utf8)

let exampleRawInput = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"

enum Instruction {
    case forward(x:Int)
    case down(x:Int)
    case up(x:Int)
}

func parseInput(_ input: String) -> [Instruction] {
    input.split(whereSeparator: \.isNewline).compactMap { s in
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

let input = parseInput(rawInput)
let example = parseInput(exampleRawInput)

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

func problem1(path : [Instruction]) -> Int {
    plotHoriz(path: path) * plotVert(path: path)
}

print("Example Problem 1: \(problem1(path: example))")
print("Example Problem 1: \(problem1(path: input))")

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

func problem2(path : [Instruction]) -> Int {
    plotHoriz(path: path) * plotVertUsingAim(path: path)
}

print("Example Problem 2: \(problem2(path: example))")
print("Example Problem 2: \(problem2(path: input))")


//: [Next](@next)
