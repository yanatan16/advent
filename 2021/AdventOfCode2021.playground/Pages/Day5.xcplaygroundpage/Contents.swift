//: [Previous](@previous)


import Foundation


let fileURL = Bundle.main.url(forResource: "input", withExtension: "txt")
let rawInput = try! String(contentsOf: fileURL!, encoding: String.Encoding.utf8)

let exampleRawInput = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

let example = Fast.parseInput(exampleRawInput)
// print(example.vectors)

let input = Fast.parseInput(rawInput)

print("Problem 1 (Example): \(Fast.problem1(example))")
print("Problem 1 (Real): \(Fast.problem1(input))")

print("Problem 2 (Example): \(Fast.problem2(example))")
print("Problem 2 (Real): \(Fast.problem2(input))")

//: [Next](@next)
