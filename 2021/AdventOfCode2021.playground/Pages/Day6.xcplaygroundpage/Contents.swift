//: [Previous](@previous)

import Foundation

let exampleRaw = """
example
"""

let example = parseInput(exampleRaw)
print("Input Example: \(example)")

let input = parseInput(try! readInput())

print("Example Solution 1: \(problem1(example))")

print("Real Solution 1: \(problem1(input))")

print("Example Solution 2: \(problem2(example))")

print("Real Solution 2: \(problem2(input))")

//: [Next](@next)
