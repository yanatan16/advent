//: [Previous](@previous)

import Foundation

let exampleRaw = """
3,4,3,1,2
"""

let example = parseInput(exampleRaw)
print("Input Example: \(example.ages)")

let input = parseInput(try! readInput())

print("Example Solution 1: \(Day6.problem1(example))")

print("Real Solution 1: \(Day6.problem1(input))")

print("Example Solution 2: \(Day6.problem2(example))")

print("Real Solution 2: \(Day6.problem2(input))")

//: [Next](@next)
