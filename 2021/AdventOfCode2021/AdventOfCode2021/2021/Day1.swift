//
//  Day1.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day1 : Solution {
    var exampleRawInput: String { """
199
200
208
210
200
207
240
269
260
263
"""}
    
    struct Input {
        let nums: [Int]
    }
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        Input(nums: raw.splitlines().compactMap { Int($0) })
    }
    
    func problem1(_ input: Input) -> Int {
        zip(input.nums[...(input.nums.count-1)],
            input.nums[1...])
            .filter { (x1, x2) in x2 > x1 }
            .count
    }
    
    func problem2(_ input: Input) -> Int {
        // Comparing x[0] to x[3] is equivalent to comparing sliding windows
        zip(input.nums[...(input.nums.count-3)],
            input.nums[3...])
            .filter { (x1, x4) in x4 > x1 }
            .count
    }
}
