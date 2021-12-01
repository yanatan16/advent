//: [Previous](@previous)
import Foundation

var day = 1

print("Welcome to Advent of Code Day \(day)")

let exampleInput : [Int] = [199,
                            200,
                            208,
                            210,
                            200,
                            207,
                            240,
                            269,
                            260,
                            263]

let fileURL = Bundle.main.url(forResource: "input", withExtension: "txt")
let rawInput = try! String(contentsOf: fileURL!, encoding: String.Encoding.utf8)
let input : [Int] = rawInput.split(whereSeparator: \.isNewline).compactMap { Int($0) }

// Problem 1
// Count increases in an array of ints
//
// Solution:
// zip up each number with its antecedent, filter for increases, and count the resulting array length
func countIncreases(_ input : [Int]) -> Int {
    zip(input[...(input.count-1)], input[1...]).filter { (x1, x2) in x2 > x1 }.count
}

print("Example Solution 1: \(countIncreases(exampleInput))")
print("My Solution 1: \(countIncreases(input))")

// Problem 2
// Count increases in a sliding window of size 3 of an array of ints
//
// Solution:
// Calculate an array of sliding window values by using zip to sum each tuple of 3 values
// then call countIncreases to get the number of increases of that array
func countSlidingWindowIncreases(_ input : [Int]) -> Int {
    let slidingWindows = zip(
        zip(input[...(input.count-2)], input[1...(input.count-1)]).map { $0 + $1 },
        input[2...]
    ).map { $0 + $1 }
    
    return countIncreases(slidingWindows)
}

print("Example Solution 2: \(countSlidingWindowIncreases(exampleInput))")
print("My Solution 2: \(countSlidingWindowIncreases(input))")

//: [Next](@next)
