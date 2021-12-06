//: [Previous](@previous)

import Foundation

let exampleRaw = """
example
"""

let example = parseInput(exampleRaw)
print("Input Example: \(example)")

let input = parseInput(try! readInput())

print("Example Solution 1: \(solve(example, problem1))")

print("Solution 1: \(solve(input, problem1))")

print("Example Solution 2: \(solve(example, problem2))")

print("Solution 2: \(solve(input, problem2))")

//: [Next](@next)
